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
from deepdiff import DeepDiff
import json
import io
from uuid import uuid4
import sys
import zmq
import math

try:
    import _pickle as pickle
except ImportError:
    import pickle

import traceback

from .constants import (
    ADDED, COMMITED,
    FETCHED, UP, ERROR, MODIFIED, DIFF_BINARY, DIFF_JSON)
from .exception import NetworkFrameError, DataError, ContextError, StateError
from .utils import get_state_str

CHUNK_SIZE = 2500000000


class ReplicatedDataFactory(object):
    """
    Manage the data types implementations.

    """

    def __init__(self):
        self.supported_types = []

    def register_type(
            self,
            source_type,
            implementation,
            timer=0,
            automatic=False,
            supported_types=False,
            check_common=False):
        """
        Register a new replicated datatype implementation
        """
        self.supported_types.append((source_type,
                                     implementation,
                                     timer,
                                     automatic,
                                     check_common))

    def match_type_by_instance(self, data):
        """
        Find corresponding type to the given datablock
        """
        for stypes, implementation, time, auto, check_common in self.supported_types:
            if issubclass(type(data), stypes):
                return implementation
        logging.error(f"{data} not supported for replication")

    def match_type_by_name(self, type_name):
        for stypes, implementation, time, auto, check_common in self.supported_types:
            if type_name == implementation.__name__:
                return implementation
        logging.error(f"{type_name} not supported for replication")

    def get_implementation_from_object(self, data):
        return self.match_type_by_instance(data)

    def get_implementation_from_net(self, type_name):
        """
        Re_construct a new replicated value from serialized data
        """
        return self.match_type_by_name(type_name)


class ReplicatedDatablock(object):
    """
    Datablock definition that handle object replication logic.
    PUSH: send the object over the wire
    STORE: register the object on the given replication graph
    LOAD: apply loaded changes by reference on the local copy
    DUMP: get local changes

    """

    __slots__ = [
        'uuid',             # uuid used as key      (string)
        'data',             # dcc data ref          (DCC type)
        'instance',         # raw data              (json)
        'str_type',         # data type name        (string)
        'dependencies',     # dependencies array    (string)
        'owner',            # Data owner            (string)
        'buffer',           # Serialized local buffer (bytes)
        'diff_method',      # Differential method (int)
        'state',
        'sender']            # Data state            (int)

    def __init__(
            self,
            owner=None,
            instance=None,
            str_type=None,
            uuid=None,
            data=None,
            bytes=None,
            sender=None,
            dependencies=[]):

        self.uuid = uuid if uuid else str(uuid4())
        self.owner = owner
        self.str_type = type(self).__name__
        self.buffer = None
        self.data = None
        self.instance = None

        if instance:
            self.state = ADDED
            self.instance = instance
        elif data:
            self.data = data
            self.state = COMMITED
        elif bytes:
            # Server side
            if type(self) == ReplicatedDatablock:
                self.state = UP
                self.str_type = str_type

                self.check(bytes)

                self.data = bytes  # Storing data as raw bytes on server side

            # Client side
            else:
                try:
                    self.data = self._deserialize(bytes)
                    self.state = FETCHED
                except Exception:
                    raise DataError(f"Failed to deserialize {self.uuid} data")

        self.dependencies = dependencies
        self.sender = sender

    def commit(self):
        """ Commit tracked object

            :raise ReferenceError:
            :raise StateError:
            :raise ContextError:
        """
        if self.state in [MODIFIED, ADDED, UP]:
            # try:
            self.data = self._dump(instance=self.instance)
            self.state = COMMITED
        else:
            raise StateError(f"Commit fail: data in a wrong state:{repr(self)}")
            logging.warning(f"Commit fail: data in a wrong state:{repr(self)}")

    def push(self, socket, identity=None, check_data=True):
        """ Push the node over the given socket as a multipart frame

            :raise NetworkFrameError:
            :raise DataError:
        """

        if self.state in [COMMITED, UP]:
            serialization_needed = (type(self.data) != bytes)

            serialized_data = self._serialize() if serialization_needed else self.data 

            owner = self.owner.encode()
            key = self.uuid.encode()
            rep_type = self.str_type.encode()
            dependencies = pickle.dumps(self.dependencies, protocol=4)

            # Determine chunk numbers
            ck_number = math.ceil(sys.getsizeof(serialized_data)/CHUNK_SIZE)

            if not serialized_data or \
                    not ck_number or \
                    not dependencies or \
                    not rep_type or \
                    not owner or \
                    not socket.IDENTITY:

                raise NetworkFrameError(f"Trying to push incomplete data: {repr(self)}")

            if check_data:
                self.check(serialized_data)

            # Server to specific Client case
            if identity:
                socket.send(identity, zmq.SNDMORE)

            # First step : send nodes metadata
            socket.send_multipart([socket.IDENTITY,
                                   key,
                                   owner,
                                   rep_type,
                                   pickle.dumps(ck_number, protocol=4),
                                   dependencies])

            # Second step: stream data chunks
            stream = io.BytesIO(serialized_data)

            for i in range(ck_number):
                chunk = stream.read(CHUNK_SIZE)
                if identity:
                    socket.send(identity, zmq.SNDMORE)
                socket.send_multipart([chunk])

            stream.close()
            # self.buffer = None
            self.state = UP
        else:
            logging.error(
                f"Attempting to push node in a wrong state: {repr(self)}")

    @classmethod
    def fetch(cls, socket, factory=None):
        """
        Here we reeceive data from the wire:
            - read data from the socket
            - reconstruct an instance
        """

        frame = socket.recv_multipart(0)

        # identity, uuid, owner, str_type, ck_number, dependencies
        # Load node metadata
        if len(frame) != 6:
            logging.error("Incomplete frame received")
            raise NetworkFrameError("Error fetching data")

        identity = frame[0]
        uuid = frame[1].decode()
        owner = frame[2].decode()
        str_type = frame[3].decode()
        ck_number = pickle.loads(frame[4])
        dependencies = pickle.loads(frame[5])
        dependencies = dependencies if dependencies else None

        # Rebuild data from chunks
        serialized_data = bytes()
        for i in range(ck_number):
            chunk_frame = socket.recv_multipart()
            serialized_data += chunk_frame[0]

        instance = None

        # Server side replication
        if factory is None:
            instance = ReplicatedDatablock(owner=owner,
                                           uuid=uuid,
                                           dependencies=dependencies,
                                           sender=identity,
                                           str_type=str_type,
                                           bytes=serialized_data)

        # Client side replication
        else:
            implementation = factory.get_implementation_from_net(str_type)

            instance = implementation(owner=owner,
                                      uuid=uuid,
                                      dependencies=dependencies,
                                      bytes=serialized_data)

        return instance

    def apply(self):
        """Apply stored data into the DCC
        """
        # UP in case we want to reset our instance data
        assert(self.state in [FETCHED, UP])
        logging.debug(f"Applying {self.uuid} - {self.str_type}")

        if self.instance is None:
            self.resolve()

        try:
            self._load(data=self.data, target=self.instance)
            self.state = UP
        except Exception:
            logging.error(
                f"Load {self.uuid} failed: \n {traceback.format_exc()}")

    def is_valid(self):
        raise NotImplementedError()

    def _construct(self, data=None):
        """Construct a new instance of the target object,
        assign our instance to this instance
        """
        raise NotImplementedError()

    def remove_instance(self):
        raise NotImplementedError()

    def resolve(self):
        pass

    def store(self, dict):
        """
        Store the node into the given dict
        """
        if self.uuid is not None:
            if self.uuid in dict:
                dict[self.uuid].data = self.data
                dict[self.uuid].state = self.state
                dict[self.uuid].dependencies = self.dependencies
            else:
                dict[self.uuid] = self

            return self.uuid

    def _deserialize(self, data):
        """
        BUFFER -> JSON
        """
        return pickle.loads(data)

    def _serialize(self):
        """
        JSON -> BUFFER
        """
        return pickle.dumps(self.data, protocol=4)

    def _dump(self, instance=None):
        """
        DCC -> JSON
        """
        assert(instance)

        return json.dumps(instance)

    def _load(self, data=None, target=None):
        """
        JSON -> DCC
        """
        raise NotImplementedError()

    def check(self, bytes):
        try:
            self._deserialize(bytes)
        except Exception:
            raise DataError(f"Failed to deserialize {self.uuid} data")

    def diff(self):
        """Compare stored data to the actual one.

        return True if the versions doesn't match
        """
        new_version = self._dump(instance=self.instance)
        if self.diff_method == DIFF_JSON:
            diff = DeepDiff(self.data, new_version, cache_size=5000)
        elif self.diff_method == DIFF_BINARY:
            diff = pickle.dumps(self.data, protocol=4) != pickle.dumps(new_version, protocol=4)
        
        return diff

    def has_changed(self):
        # TODO: marked for refactor with the repository update
        changes = self.diff()

        if changes:
            logging.debug(
                f"Found a diff on {self.uuid} ({self.str_type}): \n {changes}")
            logging.debug(f"Mark {self.uuid} as modified")
            self.state = MODIFIED

        return changes

    def resolve_deps(self):
        """Return a list of dependencies
        """
        return []

    def add_dependency(self, dependency):
        if not self.dependencies:
            self.dependencies = []
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)

    def __repr__(self):
        return f"- uuid: {self.uuid} \n \
                 - owner: {self.owner} \n \
                 - state: {get_state_str(self.state)} \n \
                 - type: {self.str_type} \n \
                 - data: {self.data if hasattr(self, 'data') else 'Empty'} \n \
                 - deps: {self.dependencies}"


class ReplicatedCommandFactory(object):
    """
    Manage the data types implementations.

    """

    def __init__(self):
        self.supported_types = []

        self.register_type(RepDeleteCommand, RepDeleteCommand)
        self.register_type(RepRightCommand, RepRightCommand)
        self.register_type(RepConfigCommand, RepConfigCommand)
        self.register_type(RepSnapshotCommand, RepSnapshotCommand)
        self.register_type(RepServerSnapshotCommand, RepServerSnapshotCommand)
        self.register_type(RepAuthCommand, RepAuthCommand)
        self.register_type(RepDisconnectCommand, RepDisconnectCommand)
        self.register_type(RepKickCommand, RepKickCommand)
        self.register_type(RepUpdateClientsState, RepUpdateClientsState)
        self.register_type(RepUpdateUserMetadata, RepUpdateUserMetadata)

    def register_type(
            self,
            source_type,
            implementation):
        """
        Register a new replicated datatype implementation
        """
        self.supported_types.append(
            (source_type, implementation))

    def match_type_by_name(self, type_name):
        for stypes, implementation in self.supported_types:
            if type_name == implementation.__name__:
                return implementation
        logging.error(f"{type_name} not supported for replication")

    def get_implementation_from_object(self, data):
        return self.match_type_by_instance(data)

    def get_implementation_from_net(self, type_name):
        """
        Re_construct a new replicated value from serialized data
        """
        return self.match_type_by_name(type_name)


class ReplicatedCommand():
    def __init__(
            self,
            owner=None,
            data=None):
        assert(owner)

        self.owner = owner
        self.data = data
        self.str_type = type(self).__name__

    def push(self, socket):
        """
        Here send data over the wire:
            - _serialize the data
            - send them as a multipart frame thought the given socket
        """
        data = pickle.dumps(self.data, protocol=4)
        owner = self.owner.encode()
        type = self.str_type.encode()

        socket.send_multipart([owner, type, data])

    @classmethod
    def fetch(cls, socket, factory=None):
        """
        Here we reeceive data from the wire:
            - read data from the socket
            - reconstruct an instance
        """

        owner, str_type, data = socket.recv_multipart(0)

        str_type = str_type.decode()
        owner = owner.decode()
        data = pickle.loads(data)

        implementation = factory.get_implementation_from_net(str_type)

        instance = implementation(owner=owner, data=data)
        return instance

    @classmethod
    def server_fetch(cls, socket, factory=None):
        """
        Here we reeceive data from the wire:
            - read data from the socket
            - reconstruct an instance
        """
        instance = None
        frame = socket.recv_multipart(0)

        if len(frame) != 4:
            logging.error(
                f"Malformed command frame received (len: {len(frame)}/4)")
            raise NetworkFrameError("Error fetching command")
        else:
            str_type = frame[2].decode()
            owner = frame[1].decode()
            data = pickle.loads(frame[3])

            implementation = factory.get_implementation_from_net(str_type)

            instance = implementation(owner=owner, data=data)
            instance.sender = frame[0]

        return instance

    def execute(self, graph):
        raise NotImplementedError()


class RepDeleteCommand(ReplicatedCommand):
    def execute(self, graph):
        assert(self.data)

        if graph and self.data in graph.keys():
            # Clean all reference to this node
            for key, value in graph.items():
                if value.dependencies and self.data in value.dependencies:
                    value.dependencies.remove(self.data)
            # Remove the node itself
            del graph[self.data]


class RepRightCommand(ReplicatedCommand):
    def execute(self, graph):
        assert(self.data)

        if graph and self.data['uuid'] in graph.keys():
            graph[self.data['uuid']].owner = self.data['owner']


class RepConfigCommand(ReplicatedCommand):
    pass


class RepSnapshotCommand(ReplicatedCommand):
    pass


class RepServerSnapshotCommand(ReplicatedCommand):
    pass


class RepAuthCommand(ReplicatedCommand):
    pass


class RepDisconnectCommand(ReplicatedCommand):
    pass


class RepKickCommand(ReplicatedCommand):
    pass


class RepUpdateClientsState(ReplicatedCommand):
    pass


class RepUpdateUserMetadata(ReplicatedCommand):
    pass
