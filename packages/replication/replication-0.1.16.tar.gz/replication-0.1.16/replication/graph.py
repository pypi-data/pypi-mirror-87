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


import collections
import threading

class ReplicationGraph(collections.MutableMapping):
    """
    Structure to hold replicated data relation graph
    """

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.lock = threading.Lock()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        with self.lock:
            return self.store[key]

    def __setitem__(self, key, value):
        with self.lock:
            self.store[key] = value

    def __delitem__(self, key):
        with self.lock:
            del self.store[key]

    def __iter__(self):
        with self.lock:
            return iter(self.store)

    def __len__(self):
        with self.lock:
            return len(self.store)

    def __repr__(self):
        str = "\n"
        for key, item in self.store.items():
            str += repr(item)
        return str

    def list(self, filter_state=None, filter_type=None):
        if filter_state:
            return [key for key, item in self.store.items()
                    if item.state == filter_state]
        if filter_type:
            return [key for key, item in self.store.items()
                    if isinstance(item, filter_type)]
        return [key for key, item in self.store.items()]

    def get_dependencies(self, node, deps=[]):
        node_ref = self.get(node)
        
        if node_ref and node_ref.dependencies:
            for child in node_ref.dependencies:
                if child not in deps:
                    deps.append(child)
                self.get_dependencies(child, deps)
    
    def find_parents(self, node_id):
        assert(node_id)
        
        parents = []

        for node in self.list():
            deps = self.get(node).dependencies
            if deps and node_id  in deps:
                parents.append(node)
        
        return parents

    def get_leaves(self):
        leaves = []

        for node in self.store.values():
            if node.dependencies is None and not self.find_parents(node.uuid):
                leaves.append(node.uuid)
        
        return leaves

    def get_roots(self):
        childs = []
        for node in self.store.values():
            if node.dependencies:
                for dep in node.dependencies:
                    if dep not in childs:
                        childs.append(dep)
        return [n for n in self.store.keys() if n not in childs]

    def bfs_from_node(self, start_node):
        visited = []
        queue = start_node

        while queue:
            current = queue.pop(0)

            if current not in visited:
                visited.append(current)
                current_ref = self.store.get(current)
                if current_ref and current_ref.dependencies:
                    queue.extend(current_ref.dependencies)
        
        return visited

    def list_ordered(self):
        nodes_list = []

        roots = self.get_roots()
        
        return reversed(self.bfs_from_node(roots))

    def get_dependencies_ordered(self, node):
        assert(node)

        deps = []
        self.get_dependencies(node, deps=deps)

        return reversed(deps)

    def get_nodes_in_state(self, state=None):
        added_items = self.list(filter_state=state)
        selected_nodes = []

        for item in added_items:
            item_deps = []
            self.get_dependencies(item, deps=item_deps)

            for deps in item_deps:
                if deps not in selected_nodes and self.store[deps].state == state:
                    selected_nodes.append(deps)

            if item not in selected_nodes and self.store[item].state == state:
                selected_nodes.append(item)
        
        return selected_nodes