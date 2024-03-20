from packet import Packet

class Node():
    def __init__(self, id):
        self.up = True # https://edstem.org/au/courses/15078/discussion/1775924
            # we assume that all nodes start up successfully
        self.id = id
        self.neighbour_costs = {}
        # store the neighbour cost and store if that neighbour is "up"

        # The reachability matrix should have each node in the network
        # as its keys, and the values should be the total cost to reach
        # that node, as well as the path. PROBABLY NOT THIS
        # Maybe each node should store the neighbour costs of every
        # other node, so each node needs only to broadcast the link cost
        # of it's neighbour nodes.
        self.reachability_matrix = {self.id : {}}
        # this may not be allowed, as the node should not have global knowledge
        self.recalculate_routing_trigger = True
        # and the shortest path dictionary actually is the result of the
        # shortest path algorithm
        self.shortest_paths = {}
        pass

    def set_neighbour_costs(self, key, cost):
        self.neighbour_costs[key] = cost
        self.reachability_matrix = {self.id : self.neighbour_costs}
        for neighbour in self.neighbour_costs.keys():
            if neighbour in self.reachability_matrix.keys():
                self.reachability_matrix[neighbour][self.id] = self.neighbour_costs[neighbour]
            else:
                self.reachability_matrix[neighbour] = {self.id : self.neighbour_costs[neighbour]}

    def get_neighbour_ids(self):
        return self.neighbour_costs.keys()

    def calculate_shortest_paths(self):
        distances = {}
        paths = {}
        for neighbour in self.reachability_matrix.keys():
            distances[neighbour] = 99999999
            paths[neighbour] = [99999999]
        shortest_paths[self.id] = [0, [self.id]]

        # Dijkstra's algorithm
        



        for neighbour in self.neighbour_costs.keys():
            shortest_paths[neighbour] = [self.neighbour_costs[neighbour], [self.id, neighbour]]
        
        while len(shortest_paths.keys()) < len(self.reachability_matrix):
            for node1 in shortest_paths.keys():
                if node1 == shortest_paths[node1][1][-1]:
                    continue
                sub_path = shortest_paths[node1]
                for node_n in self.reachability_matrix[node1]:
                    total_cost = sub_path[0] + self.reachability_matrix[node_n][node1]
                    total_path = sub_path[1]
                    total_path.append(node_n)
                    if not node_n in shortest_paths.keys():
                        shortest_paths[node_n] = [total_cost, total_path]
                    else:
                        if total_cost < shortest_paths[node_n][0]:
                            shortest_paths[node_n] = [total_cost, total_path]
        print("LOOK AT ME LOOK AT ME LOOK AT ME LOOK AT ME LOOK AT ME LOOK AT ME LOOK AT ME ")
        print("shortest paths:", shortest_paths)
        return shortest_paths
        pass

    def get_reachability_matrix(self):
        return self.reachability_matrix

    def update_reachability_matrix(self, new_matrix):
        # Receive the matrix update from neighbour.
        # We want to incorperate this info into our own matrix.
        # However we want to ignore what they say about our own neighbour link costs

        self.reachability_matrix = new_matrix  # Incorperate what they say
        self.reachability_matrix[self.id] = self.neighbour_costs # Overwrite what they say about us
        for neighbour in self.neighbour_costs.keys():
            if neighbour in self.reachability_matrix.keys():
                self.reachability_matrix[neighbour][self.id] = self.neighbour_costs[neighbour]
            else:
                self.reachability_matrix[neighbour] = {self.id : self.neighbour_costs[neighbour]}
        print("reachability matrix:", self.reachability_matrix)
        print("neighbour costs:", self.neighbour_costs)


    def read_packet(self, packet):
        s = packet.get_source()
        d = packet.get_data()
        self.update_reachability_matrix(d)
