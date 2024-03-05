
class Packet():
    def __init__(self):
        # Note, the packet should not navigate by the
        # reachability matrix stored in its data
        # it should navigate using the reachability matrix
        # of whatever node it's currently at
        self.source = None
        self.destination = None
        self.next_hop = None
        self.source_data = None

    def to_bits(self):
        pass # TODO
    def from_bits(self, bits):
        pass # TODO
    def get_destination(self):  return self.destination
    def get_source(self):       return self.source
    def get_next_hop(self):     return self.next_hop
    def unpack_data(self):      return self.source_data
    def set_next_hop(self, n):  self.next_hop = n
