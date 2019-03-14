class Graph:
    def __init__(self, graph=None):
        if graph is None:
            graph = {}

        self.graph = graph


    def get_nodes(self):
        return list(self.graph.keys())


    def get_edges(self):
        edges = []

        for node in self.graph:
            for next_node in self.graph[node]:
                if {next_node, node} not in edges:
                    edges.append({node, next_node})

        return edges


    def add_nodes(self, node):
        if node not in self.graph:
            self.graph[node] = []


    def add_edges(self, edge):
        edge = set(edge)
        (node_a, node_b) = tuple(edge)

        if node_a in self.graph:
            self.graph[node_a].append[node_b]
        else:
            self.graph[node_a] = [node_b]


    def find_paths(self, start, end, path=[]):
        path = path + [start]

        if start == end:
            return [path]

        if start not in self.graph:
            return []

        paths = []

        for node in self.graph[start]:
            if node not in path:
                new_paths = self.find_paths(self, node, end, path)

                for new_path in new_paths:
                    paths.append(new_path)

        return paths


    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]

        if start == end:
            return path
        if not self.graph.has_key(start):
            return None

        shortest_path = None

        for node in self.graph[start]:
            if node not in path:
                new_path = self.find_shortest_path(self, node, end, path)

                if new_path:
                    if not shortest_path or len(new_path) < len(shortest_path):
                        shortest_path = new_path

        return shortest_path
