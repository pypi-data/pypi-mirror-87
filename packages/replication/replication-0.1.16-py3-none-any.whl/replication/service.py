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
try:
    import _pickle as pickle
except ImportError:
    import pickle

import subprocess
import sys
import threading
import time

import zmq

from .constants import STATE_ACTIVE, STATE_INITIAL
from .exception import ServiceNetworkError
from .utils import current_milli_time


"""
 A simple service management API with two components:
   * Service Manager (ROUTER)
   * Service (DEALER)

 The goal is to manage Subprocess and Thread services by using zmq to 
 communicate between the service manager and service.
"""


class ServiceManager():
    """
        Handle Services management.
    """
    def __init__(
            self,
            python_path=sys.executable,
            ipc_port=5590):
        self._services = {}
        self._context = zmq.Context()
        self._state = STATE_INITIAL
        self._python = python_path

    def start(self, ipc_port):
        """
            Start the service manager.

            :param ipc_port: inter-service communication port 
            :type ipc_port: integer
        """
        # Bind a ROUTER socket to listen services
        self._ipc_port = ipc_port
        self._com_services = self._context.socket(zmq.ROUTER)
        self._com_services.setsockopt(zmq.IDENTITY, b'SERVICE_MANAGER')

        try:
            self._com_services.bind(f"tcp://*:{ipc_port}")
        except zmq.ZMQError:
            self._context.destroy()
            raise ServiceNetworkError(f"Can't launch service manager, an instance is already running on the same IPC ports.")

        self._com_services.linger = 0
        self._services_poller = zmq.Poller()
        self._services_poller.register(self._com_services, zmq.POLLIN)

        self._state = STATE_ACTIVE
        logging.debug('Service manager launched')

    def launch_service_as_subprocess(self, name, script_path, *args):
        """
            launch a service as subprocess

            :param name: service name
            :type name: str
            :param script_path: python script path
            :type script_path: str 
        """
        service_instance = subprocess.Popen([
            self._python,
            script_path,
            *args])

        self._services[name] = {
            'instance': service_instance,
            'state': STATE_INITIAL
        }

    def launch_service(self, service, **kwargs):
        """
            launch a service

            :param service: service implementation
            :type service: Service 
        """

        service_instance = service(ipc_port=self._ipc_port, **kwargs)

        self._services[service_instance.name] = {
            'instance': service_instance,
            'state': STATE_INITIAL
        }

    def stop_service(self, service_name):
        """
            Stop the given service

            :param service_name: Stoped service name
            :type service_name: str
        """
        assert(service_name in self._services.keys())

        service = self._services.get(service_name)

        if service:
            logging.debug(f"Stopping {service_name}....")
            self._com_services.send(service_name.encode(), zmq.SNDMORE)
            self._com_services.send_multipart([b'SERVICE/STOP', b'-'])
        else:
            logging.error(f"Service {service_name} not found")

    def stop_all_services(self):
        """
            Stop all services
        """
        for service in self._services:
            self.stop_service(service)

    def handle_services_com(self, timeout=1):
        """
            Retrieve services communications frames.

            :param timeout: Timeout delay for services message reception (milliseconds) 
            :type timeout: integer
        """
        # Services communication triage
        items = dict(self._services_poller.poll(timeout))
        service_frame = None

        if items:
            service_frame = self._com_services.recv_multipart(0)

            sender = service_frame.pop(0).decode()
            destination = service_frame.pop(0).decode()
            state = pickle.loads(service_frame.pop(0))

            if destination == "MANAGER":
                address = state.pop(0)
                if 'STATE' in address:
                    if sender not in self._services:
                        self._services[sender] = {}
                    self._services[sender]['state'] = state.pop(0)

                return None
            else:
                return [sender, state]

    def send_to_service(self, service_name, state):
        self._com_services.send(service_name.encode(), zmq.SNDMORE)
        self._com_services.send_multipart([b'IMPLEMENTATION', pickle.dumps(state, protocol=4)])

    def stop(self):
        """Stop service manager, close imternal communication sockets
        """
        assert([s['state'] == STATE_INITIAL for s in self._services.values()])

        self._com_services.close()
        logging.debug("Service manager stopped.")

        self._services.clear()

    def ensure_all_services_running(self):
        for service in self._services.values():
            inst = service.get('instance')

            if isinstance(inst ,threading.Thread) and not inst.is_alive():
                return False
            elif isinstance(inst ,subprocess.Popen) and inst.poll() is not None:
                return False
        
        return True



class Service(threading.Thread):
    """A basic looping routine.
    """
    def __init__(
            self,
            ipc_port=None,
            name="DefaultServiceName",
            loop_interval=10,
            context=zmq.Context()):
        assert(ipc_port)

        threading.Thread.__init__(self)

        self._name = name
        self._service_state = STATE_INITIAL
        self._loop_interval = loop_interval # TODO: remove this
        self._ipc_port = ipc_port
        self._context = context

        self._ipc_com = self._context.socket(zmq.DEALER)
        self._ipc_com.setsockopt(zmq.IDENTITY, self._name.encode())
        self._ipc_com.connect(f"tcp://localhost:{self._ipc_port}")
        self._ipc_com.linger = 0

        self._poller = zmq.Poller()
        self._poller.register(self._ipc_com, zmq.POLLIN)

        self._stop_flag = threading.Event()
        self.notify_manager(['STATE', self._service_state])

    def notify_manager(self, state):
        """
            Send a state to the Service Manager

            :param state: state 
            :type state: any pickleable python object
        """
        self._ipc_com.send_multipart([b'MANAGER', pickle.dumps(state, protocol=4)])

    def notify(self, state):
        """
            Send a state to the entity which run the service manager

            :param state: state 
            :type state: any pickleable python object
        """
        self._ipc_com.send_multipart([b'PARENT', pickle.dumps(state, protocol=4)])

    def run(self):
        """
            Main service loop. 
            It handle service IO communication on each iteration.
        """
        self._service_state = STATE_ACTIVE
        self.notify_manager(['STATE', self._service_state])
        
        while not self._stop_flag.is_set():
            sockets = dict(self._poller.poll(self._loop_interval))

            if self._ipc_com in sockets:
                msg = self._ipc_com.recv_multipart()
                addr = msg.pop(0).decode()
                
                if 'SERVICE' in addr:
                    if 'STOP' in addr:
                        logging.debug(f"Stopping {self._name}")
                        self._stop_flag.set()
                        break
                elif 'IMPLEMENTATION' in addr:
                    content = pickle.loads(msg.pop(0))
                    self.handle_communcation(content)
            # Run implementation tasks
            self.main(sockets)

        self.stop()
        self._service_state = STATE_INITIAL
        self._ipc_com.close()

    def handle_communcation(self, msg):
        """
            Service direct message handler

            :param msg: message
            :type msg: list
        """
        pass

    def main(self, sockets):
        """
            Service main code. Called with `_loop_interval` frequency.

            :param sockets: incoming sockets
            :type sockets: dict of zmq.Socket
        """
        raise NotImplementedError

    def stop(self):
        """
            Handle service stop. 
            Clean the room form here.
        """
        raise NotImplementedError

    @property
    def context(self):
        """ Service zmq context access
        """
        return self._context

    @property
    def poller(self):
        """ Service zmq poller access
        """
        return self._poller

    @property
    def name(self):
        """ Service name context access
        """
        return self._name
