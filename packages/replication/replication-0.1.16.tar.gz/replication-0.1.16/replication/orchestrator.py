# ##### BEGIN GPL LICENSE BLOCK #####
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


import logging
import os
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

import zmq

from .constants import (
    ADDED, COMMITED, FETCHED, MODIFIED, RP_COMMON, RP_STRICT, STATE_ACTIVE,
    STATE_INITIAL, STATE_QUITTING, STATE_SYNCING, STATE_LAUNCHING_SERVICES, UP,
    CONNECTION_TIMEOUT)
from .data import (
    RepDeleteCommand, RepDisconnectCommand, ReplicatedCommand,
    ReplicatedDatablock, RepRightCommand, RepUpdateClientsState,
    RepUpdateUserMetadata)
from .network import ClientNetService
from .observer import Observer, ExperimentalObserver
from .service import ServiceManager
from .utils import current_milli_time


class Orchestrator(threading.Thread):
    """Orchestrator

    Main thread in charge to coordinate each services such as
    - Network
    - Observers
    """

    def __init__(
            self,
            replication_graph=None,
            q_net_output=None,
            l_stash=None,
            session=None, # TODO: Remove !!!!!
            factory=None,
            python_path=sys.executable,
            external_update_handling=False):
        threading.Thread.__init__(self)

        self.name = "Orchestrator"

        self._exit_event = threading.Event()
        self._python = python_path  # used by subprocess popen
        self._rep_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        self._ttl_script = os.path.join(self._rep_dir, 'ttl.py')
        self._server_script = os.path.join(self._rep_dir, 'server.py')
        self._use_external_update_handling = external_update_handling
        self._context = zmq.Context()
        self._com_services = None  # inter-process communication socket
        self._connection_timeout = CONNECTION_TIMEOUT
        self._graph = replication_graph
        self._factory = factory
        self._q_net_output = q_net_output

        self._session = session
        self._online_users = {}
        self._stash = l_stash
        self._is_host = False
        self._state = {
            'STATE': STATE_INITIAL,
            'CURRENT': -1,
            'TOTAL': -1
        }

        self._services = []
        self._server_process = None
        self._service_manager = ServiceManager(python_path=self._python)

        self._client_uuid = uuid.uuid4()

    def connect(
            self,
            id="Default",
            address="127.0.0.1",
            port=5560,
            ipc_port=5565,
            timeout=CONNECTION_TIMEOUT,
            password=None):

        self._port = port
        self._ipc_port = ipc_port
        self._address = address
        self._connection_timeout = timeout

        self._service_manager.start(ipc_port)
        self.start()

        self._state['STATE'] = STATE_LAUNCHING_SERVICES

        self._service_manager.launch_service_as_subprocess(
                    'TTL',
                    self._ttl_script,
                    '-p', str(self._port),
                    '-d', self._address,
                    '-i', str(self._client_uuid),
                    '-t', str(timeout),
                    '-tp', str(self._ipc_port),
                )

        # Network IO service
        self._service_manager.launch_service(
            ClientNetService,
            store_reference=self._graph,
            factory=self._factory,
            items_to_push=self._q_net_output,
            id=id,
            cli_uuid=self._client_uuid,
            address=address,
            port=port,
            password=password,
            timeout=self._connection_timeout,
        )

    def host(
            self,
            id="Default",
            port=5560,
            ipc_port=5560,
            timeout=CONNECTION_TIMEOUT,
            password="admin",
            cache_directory='',
            server_log_level='INFO'):
            

        self._is_host = True
        # Launch the server
        self._server_process = subprocess.Popen([
            self._python,
            self._server_script,
            '-p', str(port),
            '-t', str(timeout),
            '-pwd', str(password),
            '--attached',
            '--log-level', server_log_level,
            '--log-file', os.path.join(cache_directory, 'multiuser_server.log')]
        )

        # Launch the client
        self.connect(
            id=id,
            address="127.0.0.1",
            port=port,
            ipc_port=ipc_port,
            password=password,
            timeout=timeout)

    def disconnect(self):
        self.stop()

    #TODO: move this into the future repositoy class
    def init_repository(self):
        self._service_manager._services['NetworkIO']['instance'].request_server_repository_init()

    def run(self):
        starting_time = current_milli_time()  # used for timeout

        while not self._exit_event.wait(.005):
            incoming_services_msg = self._service_manager.handle_services_com()

            if incoming_services_msg is not None:
                sender = incoming_services_msg.pop(0)
                content =  incoming_services_msg.pop(0)
                address = content.pop(0)

                if 'EVENT' in address:
                    if 'LOBBY' in address:
                        if self._is_host:
                            self.init_repository()

                    if 'CONNECTED' in address:
                        # Preload the graph before apply it on client side.
                        # It avoid to deal with circular dependencies.
                        self._session.call_registered('on_connection')

                        self._state = {
                            'STATE': STATE_ACTIVE,
                            'CURRENT': -1,
                            'TOTAL': -1
                        }
                        
                        if self._use_external_update_handling:
                            self._service_manager.launch_service( ExperimentalObserver,
                                                            store_reference=self._graph,
                                                            session_instance=self._session)
                        else:
                            for stype, implementation, timer, auto, check_common in self._factory.supported_types:
                                if timer > 0:
                                    self._service_manager.launch_service(Observer,
                                                                        store_reference=self._graph,
                                                                        watched_type=implementation,
                                                                        timeout=timer,
                                                                        automatic=auto,
                                                                        check_common=check_common,
                                                                        session_instance=self._session)


                    if 'FAILURE' in address:
                        logging.error(
                            "Failed to connect, authentification refused.")
                        self.stop(exit_reason="authentification refused")
                    if 'DISCONNECT' in address:
                        state = content.pop(0)
                        self.stop(exit_reason=state['reason'])
                    if 'CONNECTION_REFUSED' in address:
                        state = content.pop(0)
                        logging.error(f"Connection refused by server [ {state['reason']} ] ")
                        self.stop(exit_reason=state['reason'])
                    if 'CONNECTION_FAILED' in address:
                        logging.error("Connection failed, server not found")
                        self.stop(exit_reason='server not found')
                    if 'REQUEST_STASH' in address:
                        stash = self._stash.copy()
                        self._stash.clear()
                        self._service_manager.send_to_service(sender, stash)
                        
                elif 'STATE' in address:
                    state = content.pop(0)

                    if 'CLIENTS' in address:
                        self._online_users = state
                    if 'CONNECTION' in address:
                        self._state = state

            if self._state['STATE'] == STATE_LAUNCHING_SERVICES and \
                    current_milli_time() - starting_time > self._connection_timeout:
                logging.error("Service launching error.")
                self.stop()
            elif self.state['STATE'] == STATE_ACTIVE and \
                not self._service_manager.ensure_all_services_running():
                    logging.error("A service as stopped, disconnecting.")
                    self.stop(exit_reason="a service crashed")
        self._service_manager.stop()
        self._state['STATE'] = STATE_INITIAL

    @property
    def state(self):
        return self._state

    @property
    def services_state(self):
        return {k: v['state'] for k, v in self._service_manager._services.items()}

    @property
    def online_users(self):
        return self._online_users

    def stop(self, exit_reason="user"):
        logging.info(f"Exiting the session. Reason: {exit_reason}")
        self._session.call_registered('on_exit', reason=exit_reason)

        self._state['STATE'] = STATE_QUITTING

        # Stop the server
        if self._is_host:
            self._server_process.kill()

        self._service_manager.stop_all_services()
        self._exit_event.set()

        # Cleanup  vars
        self._online_users.clear()
        self._graph.clear()

        with self._q_net_output.mutex:
            self._q_net_output.queue.clear()

        self._is_host = False

        if not self.is_alive():
            self._service_manager._services.clear()
            self._state['STATE'] = STATE_INITIAL
