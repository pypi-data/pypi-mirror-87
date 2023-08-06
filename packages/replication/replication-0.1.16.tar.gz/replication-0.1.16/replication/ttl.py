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
import threading
import time
import zmq
import argparse
import uuid
import sys
import os
from pathlib import Path

# Quick ugly fix.
replication_lib = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(str(replication_lib.parent))
# TODO: organise modules properly

from replication.service import Service
from replication.constants import CONNECTION_TIMEOUT
from replication.utils import assert_parent_process_running

logger = logging.getLogger(__name__)
class ClientTTL(Service):
    def __init__(
            self,
            context=zmq.Context(),
            address="127.0.0.1",
            id=None,
            port=5562,
            ipc_port=5562,
            timeout=CONNECTION_TIMEOUT):

        Service.__init__(
            self,
            ipc_port=ipc_port,
            name="TTL"
        )
        # Networking
        self._id = uuid.UUID(id).bytes 

        self._command = self.context.socket(zmq.DEALER)
        self._command.setsockopt(zmq.IDENTITY, self._id)
        self._command.connect(f"tcp://{address}:{port+3}")
        self._command.linger = 0
        self._loop_interval = timeout+1000

        self.poller.register(self._command, zmq.POLLIN)

        self._command.send(b"INIT")
        
        self.start()

    def main(self, sockets):
        assert_parent_process_running()
   
        if self._command in sockets:
            self._command.recv()
            self._command.send(b"PONG")
        else:
            self.notify(['EVENT/DISCONNECT', {'reason':'connection timeout'}])         

    def stop(self):
        self._command.close()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', required=True,
                        help="port to listen")
    parser.add_argument('-d', '--destination', required=True,
                        help="address to listen")
    parser.add_argument('-i', '--id', required=True,
                        help="user id")
    parser.add_argument('-t', '--timeout', required=True,
                        help="timeout before disconnection")
    parser.add_argument('-tp', '--ttlport', required=True,
                        help="ttl port")

    args = parser.parse_args()

    cli_ttl_instance = ClientTTL(
        port=int(args.port),
        address=args.destination,
        id=args.id,
        timeout=int(args.timeout),
        ipc_port=int(args.ttlport)
    )
