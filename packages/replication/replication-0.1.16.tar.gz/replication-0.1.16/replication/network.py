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


import copy
import logging

try:
    import _pickle as pickle
except ImportError:
    import pickle

import queue
import threading
import time
import uuid

import zmq

from replication import __version__

from .constants import (CLIENT_PING_FREQUENCY, CONNECTION_TIMEOUT, RP_COMMON,
                        STATE_ACTIVE, STATE_AUTH, STATE_INITIAL, STATE_LOBBY,
                        STATE_SRV_SYNC, STATE_SYNCING, STATE_WAITING)
from .data import (RepAuthCommand, RepDeleteCommand, RepDisconnectCommand,
                   RepKickCommand, ReplicatedCommand, ReplicatedCommandFactory,
                   ReplicatedDatablock, RepRightCommand,
                   RepServerSnapshotCommand, RepSnapshotCommand,
                   RepUpdateClientsState, RepUpdateUserMetadata)
from .exception import DataError, NetworkFrameError, StateError
from .graph import ReplicationGraph
from .service import Service
from .utils import assert_parent_process_running, current_milli_time


class ClientNetService(Service):
    def __init__(
            self,
            store_reference=None,
            factory=None,
            items_to_push=None,
            id=None,
            cli_uuid=uuid.uuid4(),
            address='127.0.0.1',
            port=5560,
            ipc_port=5560,
            password=None,
            timeout=CONNECTION_TIMEOUT
    ):
        Service.__init__(
            self,
            name="NetworkIO",
            ipc_port=ipc_port
        )

        # Replication
        self._factory = factory
        self._store_reference = store_reference
        self._id = "None"
        self._items_to_push = items_to_push

        # Networking
        self._state = STATE_INITIAL
        self._srv_snapshot_size = 0
        self._srv_snapshot_progress = 0
        self._id = id
        # uuid needed to avoid reconnexion problems on router sockets
        self._uuid = cli_uuid.bytes
        self._connection_timeout = timeout

        logging.info(f"connecting on {address}:{port}")
        self._command = self.context.socket(zmq.DEALER)
        self._command.setsockopt(zmq.IDENTITY, self._uuid)
        self._command.connect(f"tcp://{address}:{port}")
        self._command.linger = 0

        self._subscriber = self.context.socket(zmq.DEALER)
        self._subscriber.setsockopt(zmq.IDENTITY, self._uuid)
        self._subscriber.connect(f"tcp://{address}:{port+1}")
        self._subscriber.linger = 0
        self._subscriber.setsockopt(zmq.RATE, 1000000)
        self._subscriber.setsockopt(zmq.RCVBUF, 2000000)

        self._publish = self.context.socket(zmq.PUSH)
        self._publish.setsockopt(zmq.IDENTITY, self._uuid)
        self._publish.connect(f"tcp://{address}:{port+2}")
        self._publish.linger = 0
        self._publish.setsockopt(zmq.RATE, 1000000)
        self._publish.setsockopt(zmq.SNDBUF, 2000000)

        self.poller.register(self._command, zmq.POLLIN)
        self.poller.register(self._subscriber, zmq.POLLIN)
        self._command_factory = ReplicatedCommandFactory()

        auth_type = 'ADMIN' if password else 'CLIENT'
        auth_request = RepAuthCommand(
            owner=self._id, data={
                "AUTH_TYPE": auth_type,
                "AUTH_ID": self._id,
                "PWD": password,
                "VERSION": __version__,
            })
        auth_request.push(self._command)

        self.state = STATE_AUTH
        self._connection_start_time = current_milli_time()

        # logging.info(__version__)
        self.start()

    def _assert_state(self, state):
        if self._state not in state:
            raise StateError("Client in wrong state")

    def _push_waiting_items(self):
        while not self._items_to_push.empty() and self._state != STATE_INITIAL:
            node = self._items_to_push.get(False)

            try:
                if isinstance(node, ReplicatedCommand):
                    node.push(self._command)
                else:
                    node.push(self._publish)

                    if self.state == STATE_SRV_SYNC:
                        # START TO PUSH TO THE SERVER
                        self._srv_snapshot_progress += 1

                        self.notify_state(
                            current=self._srv_snapshot_progress,
                            total=self._srv_snapshot_size
                        )

                        if self._srv_snapshot_progress == self._srv_snapshot_size:
                            snapshot_end = RepServerSnapshotCommand(
                                owner='server',
                                data='SNAPSHOT_END')
                            snapshot_end.push(self._command)
                            self.state = STATE_ACTIVE
                            self.notify_event('CONNECTED')

            except Exception as e:
                logging.error(f"Failed to push, cause: {e}\n {repr(node)}")

    def notify_state(self, current=-1, total=-1):
        """ Notify the ochestrator about a change of state

        :param current: current state progression counter
        :type current: int
        :param total: current state total counter
        :type total: int
        """
        state = {
            'STATE': self.state,
            'CURRENT': current,
            'TOTAL': total
        }
        self.notify(['STATE/CONNECTION', state])

    def notify_event(self, event_path):
        """ Notify the orchestrator of an event

        :param event_path: event identifer
        :type event_path: str
        """
        self.notify([f"EVENT/{event_path}"])

    def request_snapshot_init(self):
        """ Ask to the server for repository init. """

        logging.info('Requestion snapshots init')

        self._snapshot_progress = 0
        self._snapshot_total = 0

        snapshot_request = RepSnapshotCommand(
            owner=self._id,
            data={'STATE': "REQUEST_INIT"})

        snapshot_request.push(self._command)

    def request_server_repository_init(self):
        """ Ask to the server for repository init.

            :param command: incoming command
            :type command: RepAuthCommand
        """
        logging.info('Request server init')

        self._srv_snapshot_size = len(self._store_reference)
        keys = [k for k, v in self._store_reference.items()]
        assert(self._srv_snapshot_size > 0)

        snapshot_cmd = RepServerSnapshotCommand(
            owner='server',
            data={'STATE': 'INIT',
                  'SIZE': self._srv_snapshot_size,
                  'NODES': keys})
        snapshot_cmd.push(self._command)

        self.state = STATE_SRV_SYNC

    def handle_authentification(self, command):
        """ Manage client authentification

            :param command: incoming command
            :type command: RepAuthCommand
        """
        self._assert_state([STATE_AUTH])

        connection_status = command.data

        if 'LOBBY' in connection_status:
            self.state = STATE_LOBBY
            self.notify_event('LOBBY')
        if 'RUNNING' in connection_status:
            self.state = STATE_LOBBY
            self.request_snapshot_init()
        if 'FAILED' in connection_status:
            self.notify([
                'EVENT/CONNECTION_REFUSED',
                {'reason': connection_status.split(':')[1]}])

    def handle_client_snapshot(self, command):
        """ Manage incoming snapshot commands

            :param command: incoming command
            :type command: RepSnapshotCommand
        """
        self._assert_state([STATE_SYNCING, STATE_LOBBY])

        snapshot_state = command.data['STATE']
        if snapshot_state == 'INIT':
            logging.info("client init")
            self._snapshot_progress = 0
            self._snapshot_catalog = command.data.get('CATALOG')
            self._snapshot_total = len(self._snapshot_catalog)
            self._snapshot_late_updates = queue.Queue()

            self.notify_state(
                current=self._snapshot_progress,
                total=self._snapshot_total
            )

            self._current_snapshot = self._snapshot_catalog.pop()
            self.get_snapshot(self._current_snapshot)

            self.state = STATE_SYNCING

    def handle_server_repository_init(self, command):
        """ Manage server initialization commands

            :param command: incoming command
            :type command: RepServerSnapshotCommand
        """
        self._assert_state([STATE_SRV_SYNC])

        cli_snapshot_state = command.data.get('STATE')

        if cli_snapshot_state == 'ACCEPTED':
            for index, node in enumerate(self._store_reference.values()):
                node.commit()
                node._serialize()
                node.push(self._publish)
                self.notify_state(
                    current=index,
                    total=len(self._store_reference)
                )

            snapshot_cmd = RepServerSnapshotCommand(
                owner='server',
                data={'STATE': 'END'})
            snapshot_cmd.push(self._command)

        elif cli_snapshot_state == 'DONE':
            self.state = STATE_ACTIVE
            self.notify_event('CONNECTED')
        elif cli_snapshot_state == 'REJECTED':
            logging.error("client snapshot refused by the server.")
            self._state = STATE_LOBBY

    def get_snapshot(self, id):
        """ Ask a specific snapshot to the server

            :param id: uuid of the data
            :type id: str
        """
        logging.debug(f"get {id}")
        snapshot_request = RepSnapshotCommand(
            owner=self._id,
            data={
                'STATE': "GET",
                'ID': id})

        snapshot_request.push(self._command)

    def main(self, sockets):
        # DATA OUT
        if self.state in [STATE_ACTIVE, STATE_SRV_SYNC]:
            self._push_waiting_items()

        # COMMANDS I/O
        if self._command in sockets:
            try:
                command = ReplicatedCommand.fetch(
                    self._command,
                    self._command_factory)
            except Exception as e:
                logging.error(f"Corrupted frame received, skipping it. Cause:{e}")
            else:
                # AUTHENTIFICATION
                if isinstance(command, RepAuthCommand):
                    self.handle_authentification(command)

                # DISCONNECT CONFIRMATION
                if isinstance(command, RepDisconnectCommand):
                    self.notify(['EVENT/DISCONNECT', command.data])

                # CLIENTS INFO UPDATE
                if isinstance(command, RepUpdateClientsState):
                    self.notify(['STATE/CLIENTS', command.data])

                # SERVER-->CLIENT SNAPSHOT
                if isinstance(command, RepSnapshotCommand):
                    self.handle_client_snapshot(command)

                # CLIENT -> SERVER SNAPSHOT
                if isinstance(command, RepServerSnapshotCommand):
                    self.handle_server_repository_init(command)

                # GRAPH OPERATION (DELETE, CHANGE_RIGHT)
                if type(command) in [RepDeleteCommand, RepRightCommand]:
                    command.execute(self._store_reference)

        # DATA IN
        if self._subscriber in sockets:
            try:
                datablock = ReplicatedDatablock.fetch(
                    self._subscriber,
                    self._factory)
            except Exception as e:
                logging.error(f"Corrupted frame received, skipping it. Cause:{e}")
            else:
                # Client snapshot
                if self.state == STATE_SYNCING:
                    # If the snapshot is expected in the snapshot catalog we store
                    # it and ask for the next
                    if datablock.uuid == self._current_snapshot:
                        self._snapshot_progress += 1
                        self.notify_state(
                            current=self._snapshot_progress,
                            total=self._snapshot_total
                        )
                        datablock.store(self._store_reference)

                        if not self._snapshot_catalog:
                            # Apply late updates
                            while not self._snapshot_late_updates.empty():
                                late_update = self._snapshot_late_updates.get()
                                logging.info(
                                    f"Applying late update: {late_update.uuid}")
                                late_update.store(self._store_reference)

                            snapshot_request = RepSnapshotCommand(
                                owner=self._id,
                                data={'STATE': "DONE"})
                            snapshot_request.push(self._command)
                            logging.info("Snapshot done.")
                            self._state = STATE_ACTIVE
                            self.notify_event('CONNECTED')
                        else:
                            self._current_snapshot = self._snapshot_catalog.pop()
                            self.get_snapshot(self._current_snapshot)
                    # If it isn't expected why keep it in order to apply it
                    #  at the end of the snapshot process.
                    else:
                        logging.info("Adding an update for the late one...")
                        self._snapshot_late_updates.put(datablock)

                # Store received updates
                if self.state == STATE_ACTIVE:
                    datablock.store(self._store_reference)
        # Various timeout checks
        # auth
        if self.state == STATE_AUTH:
            if (current_milli_time()-self._connection_start_time) > self._connection_timeout:
                self.notify_event('CONNECTION_FAILED')

    def stop(self):
        # Exit
        self._command.close()
        self._subscriber.close()
        self._publish.close()

        self._state = STATE_INITIAL

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        self.notify_state()


class ServerNetService(threading.Thread):
    def __init__(self):

        # Threading
        threading.Thread.__init__(self)
        self.name = "Server_Network"
        self._exit_event = threading.Event()

        # Networking
        self._graph = ReplicationGraph()
        self._context = zmq.Context.instance()
        self._command = None
        self._publisher = None
        self._pull = None
        self._state = 0
        self.clients = {}
        self._ttl = None

    def listen(
            self,
            port=5560,
            password='admin',
            attached=False,
            timeout=CONNECTION_TIMEOUT):
        self._password = password
        self._port = port
        self._attached = attached

        # Update request
        self._command = self._context.socket(zmq.ROUTER)
        self._command.setsockopt(zmq.IDENTITY, b'SERVER_COMMAND')
        self._command.bind(f"tcp://*:{port}")
        self._command.linger = 0

        # Update all clients
        self._publisher = self._context.socket(zmq.ROUTER)
        self._publisher.setsockopt(zmq.IDENTITY, b'SERVER_PUSH')
        self._publisher.bind(f"tcp://*:{port+1}")
        self._publisher.linger = 0
        self._publisher.setsockopt(zmq.RATE, 1000000)
        self._publisher.setsockopt(zmq.SNDBUF, 2000000)

        # Update collector
        self._pull = self._context.socket(zmq.PULL)
        self._pull.setsockopt(zmq.IDENTITY, b'SERVER_PULL')
        self._pull.bind(f"tcp://*:{port+2}")
        self._pull.linger = 0
        self._pull.setsockopt(zmq.RATE, 1000000)
        self._pull.setsockopt(zmq.RCVBUF, 2000000)

        # TTL communication
        self._ttl_pipe = self._context.socket(zmq.DEALER)
        self._ttl_pipe.bind("inproc://server_ttl")
        self._ttl_pipe.linger = 0

        self._ttl = ServerTTL(
            port=port+3,
            timeout=timeout
        )

        self._client_snapshot_size = 0
        self._client_snapshot_progress = 0

        self.start()

    def disconnect_client(self, client, reason):
        if client in self.clients:
            leaving_client = self.clients[client]
            cleanup_commands = []
            for key, node in self._graph.items():
                if node.owner == leaving_client['id']:
                    logging.debug(f"Changing node {node.uuid} rights to COMMON")
                    cleanup_commands.append(
                        RepRightCommand(
                            owner='server',
                            data={
                                'uuid': node.uuid,
                                'owner': RP_COMMON
                            }
                        ))
            for rr_cmd in cleanup_commands:
                for cli in self.clients.keys():
                    if cli != client and not self._command._closed:
                        self._command.send(cli, zmq.SNDMORE)
                        rr_cmd.push(self._command)
                        rr_cmd.execute(self._graph)

            del self.clients[client]
            logging.info(f"{leaving_client['id']} disconnected from the server [{reason}]")
            # if len(self.clients) == 0 and self._attached:
            #     self.stop()

    def _update_clients_states(self):
        user_dict = {}
        for user, user_data in self.clients.items():
            user_dict[user_data['id']] = user_data

        clients_states = RepUpdateClientsState(
            owner='server',
            data=user_dict
        )

        # Push it to every clients
        for client_uid in self.clients:
            self._command.send(client_uid, zmq.SNDMORE)
            clients_states.push(self._command)

    def _login_client(self, auth_type, uid, id, password, version):
        """ Register a client on the server

        return:
        FAILED
        LOBBY
        RUNNING
        """

        for cli in self.clients.values():
            if id == cli['id']:
                logging.debug("client logged in")
                return 'FAILED: client already logged in'

        if auth_type == 'ADMIN' and password != self._password:
            return 'FAILED: wrong password'

        if version != __version__:
            return f'FAILED: wrong client version ({version} != {__version__})'

        logging.info(f"{id} logged in.")

        self.clients[uid] = {
            'id': id,
            'admin': auth_type == 'ADMIN',
            'latency': 999,
            'status': STATE_LOBBY,
            'metadata': {},
        }
        if self._state in [STATE_WAITING, STATE_SRV_SYNC]:
            return 'LOBBY'
        else:
            return 'RUNNING'

    def kick(self, user):
        """ kick the given user

        :arg user: username of the kicked client
        :type user: str
        """
        for k, v in self.clients.items():
            if v['id'] == user:
                disconnect = RepDisconnectCommand(
                    owner='server',
                    data={
                        'reason': 'kicked by admin',
                    }
                )
                self._command.send(k, zmq.SNDMORE)
                disconnect.push(self._command)

                self._ttl_pipe.send_multipart([b'STOP_WATCHING', k])
                self.disconnect_client(k, 'kicked')

                logging.warning(f"{user} kicked from the session.")
                return

        logging.error(f"Can't kick {user}, user not found.")

    def send_client_snapshot_init(self, client):
        catalog = [str(k) for k in self._graph.keys()]
        snapshot_state = RepSnapshotCommand(
            owner='server',
            data={
                'STATE': 'INIT',
                'CATALOG': catalog})
        logging.info(f"Pushing nodes to {self.clients[client]['id']}")
        self._command.send(client, zmq.SNDMORE)
        snapshot_state.push(self._command)

    def handle_client_snapshot(self, command):
        """ Handle client snapshot commands """

        snapshot_state = command.data.get('STATE')

        if snapshot_state == 'REQUEST_INIT':
            self.send_client_snapshot_init(command.sender)
        elif snapshot_state == 'GET':
            node = self._graph.get(command.data['ID'])
            node.push(self._publisher, identity=command.sender)
        elif snapshot_state == 'DONE':
            # Set client ready
            logging.info(f"{self.clients[command.sender]['id']} up to date.")
            self.clients[command.sender]['status'] = STATE_ACTIVE
            self._update_clients_states()

    def run(self):
        logging.info(f"Listening on {self._port}.")
        poller = zmq.Poller()

        poller.register(self._command, zmq.POLLIN)
        poller.register(self._pull, zmq.POLLIN)
        poller.register(self._ttl_pipe, zmq.POLLIN)

        command_factory = ReplicatedCommandFactory()

        self._state = STATE_WAITING

        while not self._exit_event.is_set():
            if self._attached:
                assert_parent_process_running()

            # Non blocking poller
            socks = dict(poller.poll(1000))

            # COMMAND HANDLING
            if self._command in socks:
                try:
                    command = ReplicatedCommand.server_fetch(
                        self._command, command_factory)
                except Exception as e:
                    logging.error(f"Corrupted frame received, skipping it. Cause:{e}")
                else:
                    # AUHTENTIFICATION
                    if isinstance(command, RepAuthCommand):
                        auth_type = command.data.get('AUTH_TYPE')
                        auth_origin = command.sender
                        auth_id = command.data.get('AUTH_ID')
                        auth_pass = command.data.get('PWD', None)
                        client_version = command.data.get('VERSION')

                        auth_status = self._login_client(auth_type,
                                                        auth_origin,
                                                        auth_id,
                                                        auth_pass,
                                                        client_version)

                        auth_response = RepAuthCommand(
                            owner="server",
                            data=auth_status)

                        self._update_clients_states()

                        self._command.send(command.sender, zmq.SNDMORE)
                        auth_response.push(self._command)

                    # SERVER-> CLIENT SNAPSHOT
                    if isinstance(command, RepSnapshotCommand):
                        self.handle_client_snapshot(command)

                    # CLIENT-> SERVER SNAPSHOT
                    if isinstance(command, RepServerSnapshotCommand):
                        cli_snapshot_state = command.data.get('STATE')
                        cli_snapshot_lenght = command.data.get('SIZE')
                        cli_snapshot_dict = command.data.get('NODES')

                        if cli_snapshot_state == 'INIT':
                            if self._state == STATE_SRV_SYNC:  # REJECT
                                snapshot_status = "REJECTED"
                            if self._state == STATE_WAITING:
                                snapshot_status = "ACCEPTED"
                                self._client_snapshot_size = cli_snapshot_lenght
                                self._client_snapshot_dict = cli_snapshot_dict

                            snapshot_cmd = RepServerSnapshotCommand(
                                owner='server',
                                data={'STATE': snapshot_status})
                            self._command.send(command.sender, zmq.SNDMORE)
                            snapshot_cmd.push(self._command)
                            self._state = STATE_SRV_SYNC
                        if cli_snapshot_state == 'END':
                            self.clients[command.sender]['status'] = STATE_ACTIVE
                            self._update_clients_states()
                            logging.info("Done")

                    # CLIENT METADATA
                    if isinstance(command, RepUpdateUserMetadata):
                        user = self.clients.get(command.sender)

                        if user:
                            user['metadata'].update(command.data)
                            self._update_clients_states()

                    # KICK
                    if isinstance(command, RepKickCommand):
                        self.kick(command.data['user'])

                    # OTHERS
                    if type(command) in [RepDeleteCommand, RepRightCommand]:
                        command.execute(self._graph)
                        for client_uid in self.clients:
                            if client_uid != command.sender:
                                self._command.send(client_uid, zmq.SNDMORE)
                                command.push(self._command)

            # TTL HANDLING
            if self._ttl_pipe in socks:
                notification = self._ttl_pipe.recv_multipart()

                if notification[0] == b'STATE':
                    clients_states = pickle.loads(notification[1])

                    # Prepare update
                    for id, state in clients_states.items():
                        cli = self.clients.get(id)
                        if cli:
                            cli['latency'] = state['latency']
                        else:
                            self._ttl_pipe.send_multipart(
                                [b'STOP_WATCHING', id])

                    self._update_clients_states()

                if notification[0] == b'LOST':
                    self.disconnect_client(notification[1], 'connection closed')

            # DATA HANDLING
            if self._pull in socks:
                # Regular update  routing (Clients / Server / Clients)

                try:
                    datablock = ReplicatedDatablock.fetch(self._pull)
                except Exception as e:
                    logging.error(f"Corrupted frame received, skipping it. Cause:{e}")
                else:
                    datablock.store(self._graph)

                    if self._state == STATE_ACTIVE:
                        # Update all ready clients
                        for client_uid, client_data in self.clients.items():
                            if client_uid != datablock.sender:
                                datablock.push(self._publisher,
                                               identity=client_uid,
                                               check_data=False)
                    elif self._state == STATE_SRV_SYNC:
                        self._client_snapshot_progress += 1
                        logging.info(f"Receiving snapshot {self._client_snapshot_progress}/{self._client_snapshot_size}")
                        self._client_snapshot_dict.remove(datablock.uuid)
                        if len(self._client_snapshot_dict) == 0:
                            # Launch snapshot for other waiting clients
                            snapshot_cmd = RepServerSnapshotCommand(
                                owner='server',
                                data={'STATE': 'DONE'})

                            self._command.send(command.sender, zmq.SNDMORE)
                            snapshot_cmd.push(self._command)

                            for client in self.clients.keys():
                                if client != command.sender:
                                    self.send_client_snapshot_init(client)

                            self._state = STATE_ACTIVE

        while self._ttl._state != STATE_INITIAL:
            time.sleep(1)

        self._command.close()
        self._pull.close()
        self._publisher.close()
        self._ttl_pipe.close()

    def stop(self):
        self._ttl.stop()
        self._exit_event.set()
        self._state = 0


class ServerTTL(threading.Thread):
    def __init__(
            self,
            context=zmq.Context(),
            port=5562,
            timeout=CONNECTION_TIMEOUT):
        # Threading
        threading.Thread.__init__(self)
        self.name = "server_TTL"
        self.daemon = False
        self._id = id
        self._exit_event = threading.Event()

        # Networking
        self._context = context = zmq.Context.instance()
        self._command = self._context.socket(zmq.ROUTER)
        self._command.bind(f"tcp://*:{port}")
        self._command.linger = 0
        self._pipe = self._context.socket(zmq.DEALER)
        self._pipe.connect("inproc://server_ttl")
        self._pipe.linger = 0

        self._timeout = timeout
        self._state = STATE_INITIAL
        self._clients_state = {}

        self.start()

    def run(self):
        self._state = STATE_ACTIVE
        poller = zmq.Poller()

        poller.register(self._command, zmq.POLLIN)
        poller.register(self._pipe, zmq.POLLIN)
        last_update_time = current_milli_time()
        while not self._exit_event.is_set():
            socks = dict(poller.poll(1))
            current_time = current_milli_time()

            if self._command in socks:
                identity, frame = self._command.recv_multipart(0)

                if frame == b'INIT':
                    self._clients_state[identity] = {}
                    self._clients_state[identity]['latency'] = 999
                    self._clients_state[identity]['last_received_update'] = current_time
                    self._clients_state[identity]['last_sent_update'] = current_time
                    self._command.send(identity, zmq.SNDMORE)
                    self._command.send(b"PING")

                client = self._clients_state.get(identity)

                if client is None:
                    continue

                client['last_received_update'] = current_time

            if self._pipe in socks:
                notification = self._pipe.recv_multipart()

                if notification[0] == b'STOP_WATCHING':
                    self.stop_monitor(notification[1])

            if current_time-last_update_time > 1000:
                last_update_time = current_time
                client_to_remove = []

                # Check clients status
                for client, client_data in self._clients_state.items():
                    client_data['latency'] = abs(
                        (client_data['last_received_update'])-(client_data['last_sent_update']))

                    if client_data['latency'] > self._timeout:
                        client_to_remove.append(client)
                        self._pipe.send_multipart([b'LOST', client])

                for client in client_to_remove:
                    self.stop_monitor(client)

                self._pipe.send_multipart(
                    [b'STATE', pickle.dumps(self._clients_state, protocol=4)])

            for cli_key, cli_data in self._clients_state.items():
                if (current_time-cli_data['last_received_update']) > CLIENT_PING_FREQUENCY and \
                        current_time-cli_data['last_sent_update'] > CLIENT_PING_FREQUENCY:

                    self._command.send(cli_key, zmq.SNDMORE)
                    self._command.send(b"PING")
                    cli_data['last_sent_update'] = current_time

        self._command.close()
        self._pipe.close()
        self._state = STATE_INITIAL

    def stop_monitor(self, client):
        if client in self._clients_state:
            logging.debug(f"Removing client {client} from watchlist")
            del self._clients_state[client]

    @property
    def state(self):
        return self._state

    @property
    def clients_state(self):
        return copy.copy(self._clients_state)

    def stop(self):
        self._exit_event.set()
