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
import queue
import time
import threading
import sys

from .constants import (ADDED, COMMITED, FETCHED,
                        STATE_ACTIVE, STATE_INITIAL,
                        STATE_SYNCING, UP, MODIFIED,
                        RP_COMMON, RP_STRICT)
from .data import (ReplicatedCommand, RepDeleteCommand,
                   ReplicatedDatablock, RepRightCommand,
                   RepDisconnectCommand, RepUpdateClientsState,
                   RepUpdateUserMetadata, RepKickCommand,
                   ReplicatedDataFactory)
from .graph import ReplicationGraph
from .network import (ServerNetService,
                      ServerTTL)
from .exception import NonAuthorizedOperationError, UnsupportedTypeError
from .orchestrator import Orchestrator
from .utils import get_state_str
this = sys.modules[__name__]


class Session(object):
    def __init__(self):
        self._item_to_push = queue.Queue()
        self._id = None
        self._stash = []
        self._graph = ReplicationGraph()
        self.callbacks = {}

    def configure(self,
                  factory: ReplicatedDataFactory = None,
                  python_path: str = sys.executable,
                  external_update_handling: bool = False):
        """ Session configuration 

        :param factory: Dcc data io protocol 
        :type factory: ReplicatedDataFactory
        :param python_path: python executable path (launch ttl and server) 
        :type python_path: str
        :param external_update_handling: Enable dcc driven updates.
        :type external_update_handling: bool
        """
        assert(factory)

        self._factory = factory

        self._orchestrator = Orchestrator(
            replication_graph=self._graph,
            q_net_output=self._item_to_push,
            l_stash=self._stash,
            python_path=python_path,
            session=self,
            factory=self._factory,
            external_update_handling=external_update_handling
        )

    def _assert_modification_rights(self, node=None):
        if self._graph[node].owner not in [self._id, RP_COMMON]:
            raise NonAuthorizedOperationError(
                "Not authorized to modify the node {node}")

    def _evaluate_dependencies(self, node_uuid):
        node = self._graph[node_uuid]

        assert(node)
        if not node.instance:
            return

        if node.dependencies:
            logging.debug(f"Clearing {len(node.dependencies)} dependencies.")
            node.dependencies.clear()

        dependencies = node.resolve_deps()

        logging.debug(f"found dependencies: {dependencies}")
        for dep in dependencies:
            registered_dep = self.get(reference=dep)
            if registered_dep:
                node.add_dependency(registered_dep.uuid)
            else:
                try:
                    dep_node_uuid = self.add(dep, owner=node.owner)
                except UnsupportedTypeError:
                    logging.warning(f"Skipping {type(dep)}")
                else:
                    node.add_dependency(dep_node_uuid)

    def register(self, name):
        def func_wrapper(func):
            self.callbacks[name] = func
            return func
        return func_wrapper

    def call_registered(self, name=None, **kwargs):
        func = self.callbacks.get(name, None)
        if func is None:
            logging.info("No function registered against - " + str(name))
            return None
        return func(**kwargs)

    def connect(self,
                id="Default",
                address="127.0.0.1",
                port=5560,
                ipc_port=5560,
                timeout=1000,
                password=None):
        """Connect to a session

        :param id: user name
        :type id: string
        :param address: host ip address
        :type address: string
        :param port: host port
        :type port: int
        """
        if not self._orchestrator:
            logging.error("session not configured")
            return

        self._orchestrator.connect(
            id,
            address,
            port,
            ipc_port,
            timeout=timeout,
            password=password)
        self._id = id

    def host(self,
             id="Default",
             port=5560,
             ipc_port=5569,
             timeout=1000,
             password=None,
             cache_directory='',
             server_log_level='INFO'):
        """Host a session

        :param id: user name
        :type id: string
        :param address: host ip address
        :type address: strings
        :param port: host port
        :type port: int
        """
        if not self._orchestrator:
            logging.error("session not configured")
            return

        # Create a server and serve
        self._orchestrator.host(
            id=id,
            port=port,
            ipc_port=ipc_port,
            timeout=timeout,
            password=password,
            cache_directory=cache_directory,
            server_log_level=server_log_level
        )
        self._id = id

    def init(self):
        """ Init the repository data

            commit and push initial graph to the server
        """
        if len(self._graph) == 0:
            logging.error("Add some data first")
            return

        self._orchestrator.init_repository()

    def disconnect(self):
        """Disconnect from session
        """
        self._orchestrator.disconnect()

    def add(self, object, owner=None, dependencies=[]):
        """Register a python object for replication

        :param objet: Any registered object
        :type object: Any registered object type in the given factory
        :param dependencies: Object dependencies uuid
        :type dependencies: Array of string
        """
        assert(object)

        # Retrieve corresponding implementation and init a new instance
        implementation = self._factory.get_implementation_from_object(
            object)

        if implementation:
            default_owner = RP_COMMON

            new_owner = owner if owner else default_owner

            new_node = implementation(
                owner=new_owner,
                instance=object,
                dependencies=dependencies)

            if new_node:
                dependencies = new_node.resolve_deps()

                for dependance in dependencies:
                    dep_ref = self.get(reference=dependance)
                    if dep_ref:
                        new_node.add_dependency(dep_ref.uuid)
                    else:
                        if dependance:
                            try:
                                new_child_node = self.add(object=dependance)
                                if new_child_node:
                                    new_node.add_dependency(new_child_node)
                            except UnsupportedTypeError:
                                logging.warning(f"Skipping {type(object)}.")
                logging.debug(f"Registering {object} as {new_node.uuid}")
                new_node.store(self._graph)

                return new_node.uuid
        else:
            raise UnsupportedTypeError(
                f"{type(object)} not supported, skipping.")

    def remove(self, uuid, remove_dependencies=True):
        """
        Unregister for replication the given object.

        :param uuid: node uuidñ
        :type uuid: string
        :param remove_dependencies: remove all dependencies
        :type remove_dependencies: bool (default: True)
        :raise NonAuthorizedOperationError:
        :raise KeyError:
        """
        self._assert_modification_rights(uuid)

        if self.is_registered(uuid):
            nodes_to_delete = []

            if remove_dependencies:
                nodes_to_delete.extend(
                    self._graph.get_dependencies_ordered(node=uuid))

            nodes_to_delete.append(uuid)

            logging.debug(f"Removing {nodes_to_delete}")
            for node in nodes_to_delete:
                delete_command = RepDeleteCommand(
                    owner='client', data=node)
                # remove the key from our store
                delete_command.execute(self._graph)
                self._item_to_push.put(delete_command)
        else:
            raise KeyError("Cannot unregister key")

    def kick(self, user):
        """
        Kick a user from the session.
        """

        if user == self._id:
            logging.error("You can't kick ypurself")
            return
        if self.is_admin():
            self._item_to_push.put(
                RepKickCommand(
                    owner=self._id,
                    data={
                        'user': user,
                    }
                )
            )
        else:
            logging.error("Insufisent rights to kick.")

    def commit(self, uuid):
        """Commit the given node

        :param uuid: node uuid
        :type uuid: string
        :raise ReferenceError:
        :raise StateError:
        :raise ContextError:
        """
        # TODO: refactoring
        assert(self.is_registered(uuid))

        node = self._graph.get(uuid)

        if node.state == COMMITED:
            return

        self._evaluate_dependencies(uuid)

        for dep_uuid in self._graph.get_dependencies_ordered(node=uuid):
            dep = self._graph.get(dep_uuid)
            if dep.state in [ADDED, MODIFIED]:
                dep.commit()
        node.commit()

    def push(self, uuid):
        """Replicate a given node to all users. Send all node in `COMMITED` by default.

        :param uuid: node key to push
        :type uuid: string
        """
        # TODO: Refactoring
        if uuid:
            self._assert_modification_rights(uuid)

            node = self._graph[uuid]

            for dep in self._graph.get_dependencies_ordered(node=uuid):
                dep_node = self._graph[dep]
                if dep_node.state in [COMMITED, ADDED]:
                    self._item_to_push.put(dep_node)
            self._item_to_push.put(node)

    def stash(self, uuid):
        if uuid not in self._stash:
            self._stash.append(uuid)

    def apply(self, uuid=None, force=False, force_dependencies=False):
        """Apply cached version to local object(s) instance

        :param uuid: node key to apply
        :type uuid: string
        :param force: force node apply
        :type force: bool
        :param force_dependencies: force node dependencies apply
        :type force_dependencies: bool
        """
        node = self.get(uuid=uuid)

        if node and (node.state in [FETCHED] or force):
            deps = self._graph.get_dependencies_ordered(node=uuid)

            # Apply  dependencies
            for dep in deps:
                dep_node = self.get(uuid=dep)

                if dep_node and (dep_node.state in [FETCHED] or force_dependencies):
                    dep_node.apply()

            node.apply()
        else:
            logging.warning(f"Can't apply node {uuid}, \
                             wrong state: {get_state_str(node.state)}")

    def change_owner(self,
                     uuid,
                     new_owner,
                     ignore_warnings=True,
                     affect_dependencies=True):
        """Change a node owner

        :param uuid: node key
        :type uuid: string
        :param new_owner: new owner id
        :type new_owner: string
        :param ignore_warnings: ignore NonAuthorizedOperationError 
        :type ignore_warnings: bool
        :param affect_dependencies: change dependencies owner
        :type affect_dependencies: bool

        """
        assert(self.is_registered(uuid))

        affected_nodes = []

        if affect_dependencies:
            affected_nodes.extend(self._graph.get_dependencies_ordered(node=uuid))           
        affected_nodes.append(uuid)

        for n in affected_nodes:
            try:
                self._assert_modification_rights(n)
            except NonAuthorizedOperationError as e:
                if ignore_warnings:
                    node_ref = self._graph.get(n)
                    logging.debug(f"Node {n} already owned by {node_ref.owner}")
                    continue
                else:
                    raise e
            else:
                # Setup the right override command
                right_command = RepRightCommand(
                    owner=self._id,
                    data={
                        'uuid': n,
                        'owner': new_owner}
                )
                # Apply localy
                right_command.execute(self._graph)
                # Dispatch on clients
                self._item_to_push.put(right_command)

    def get(self, uuid=None, reference=None):
        """Get a node ReplicatedDatablock instance

        :param uuid: node uuid
        :type uuid: string
        :return: ReplicatedDatablock
        """

        if uuid:
            return self._graph.get(uuid)
        if reference:
            for k, v in self._graph.items():
                if not v.instance:
                    continue
                if reference == v.instance:
                    return v
        return None

    def update_user_metadata(self, dikt):
        """Update user metadata

        Update local client informations to others (ex: localisation)

        :param json:
        :type dict:
        """
        assert(dikt)

        state_update_request = RepUpdateUserMetadata(
            owner=self._id,
            data=dikt
        )

        self._item_to_push.put(state_update_request)

    # TODO: remove
    def is_registered(self, uuid=None, reference=None):
        """Check for a node existence

        :param uuid: node uuid
        :type uuid: string
        :return: bool
        """
        if uuid:
            return uuid in self._graph.keys()
        if reference:
            for k, v in self._graph.items():
                if reference == v.instance:
                    return True

        return False

    def is_readonly(self, node_id: str)->bool:
        """ Check local user modification rights on a node

        :param node_id: node identifier
        :type node_id: str
        :return: bool
        """
        node = self.get(uuid=node_id)
        return node and (node.owner in [self._id, RP_COMMON])

    # TODO: remove
    def list(self, filter=None, filter_owner=None):
        """List all graph nodes keys
        :param filter: node type
        :type filter: ReplicatedDatablock class (or child class)
        """
        base_list = self._graph.list(filter_type=filter)
        if filter_owner:
            return [key for key in base_list
                    if self._graph[key].owner == filter_owner]
        else:
            return base_list

    @property
    def state(self):
        """Get active session state

        :return: session state
        """
        #TODO: refactor
        if hasattr(self, '_orchestrator'):
            return self._orchestrator.state
        else:
            return {'STATE': STATE_INITIAL}

    @property
    def services_state(self):
        return self._orchestrator.services_state

    @property
    def online_users(self):
        return self._orchestrator.online_users

    @property
    def id(self):
        return self._id

    def is_admin(self):
        return self.online_users[self.id]['admin']


this.session = Session()
