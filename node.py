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

        # this may not be allowed, as the node should not have global knowledge
        self.reachability_matrix = {}
        self.recalculate_routing_trigger = True
        # and the shortest path dictionary actually is the result of the
        # shortest path algorithm
        self.shortest_paths = {}
        self.in_transit_packets = []
        pass

    def set_neighbour_costs(self, key, cost):
        self.neighbour_costs[key] = cost

    def calculate_shortest_paths(self):
        pass

    def update_reachability_matrix(self):
        # Keep a checklist of which nodes need to be heard from
        # before we know we've received a packet from everyone
        # make no initial assumptions about how many nodes there
        # are in the network
        # come up with some way of noting that a node has gone down
        # or when a new node has been added.

        # Maybe come up with a phase system where each node
        # decides to stop listening to broadcasts and decides
        # that any node whos packet they havent received yet
        # has gone down
        pass

    def next_hop_in_path(destination_key):
        # give the next node in the shortest path to the
        # destination node
        assert destination_key in self.shortest_paths # this may fail. i will be
        # interested to see if we can prove that it will / wont
        next_hop = self.shortest_paths[destination_key]["path"][0]
        assert next_hop in self.neighbour_costs.keys()
        return next_hop
        # give the first step in the shortest path to the destination from this node

    def read_packet(self, packet):
        s = packet.get_source()
        d = packet.unpack_data()
        if d != self.reachability_matrix[packet.s]:
            self.recalculate_routing_trigger = True # this is gonna need a lock on it
            self.reachability_matrix[packet.s] = d
            self.update_reachability_matrix() # is this not the same as the line above?
        # update the reachability matrix for this node
        # based on the information contained in this
        # packet

    def recieve_packet(packet):
        if packet.get_destination() == self.id:
            self.read_packet(packet)
        else:
            packet.set_next_hop(self.next_hop_in_path(packet.get_destination()))
            self.in_transit_packets.append(packet)

    def get_outgoing_packets(self):
        # generate all of the packets to be sent from this
        # node and also add on all the packets that are passing
        # through this node
        outgoing = self.in_transit_packets
        self.in_transit_packets = []
        return outgoing + self.generate_packets()

    def generate_packets(self):
        return []
