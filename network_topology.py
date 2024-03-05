import random, os

class linkCountException(Exception):
    pass

class Node():
    def __init__(self, id, port = 0):
        print(id, port)
        self.id = id
        self.port = port
        self.neighbours = {}


""" NOTE:
    it may be better eventually to represent the links as a cost matrix
    """
class Network():
    def __init__(self, node_count = 10, link_count = 15):
        if link_count < node_count:
            raise linkCountException
        # Node ids are letters A-J
        # Node ports are numbers 6000-6010
        # Link cost ranges from 0.5 to 10.0
        node_ids = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self.nodes = [Node(node_ids[i],i+6000) for i in range(10)]
        # first generate a random spanning tree
        # then add in edges randomly til the limit has been satisfied
        for i in range(1,len(self.nodes)):
            n1 = self.nodes[i]
            n2 = self.nodes[random.randint(0,i-1)]
            self.add_link(n1,n2)

        extra_links = 0
        print("extwa winks")
        while extra_links < link_count - node_count:
            n1_index = random.randint(0,node_count-1) # this is awesome, check
            n1 = self.nodes[n1_index]
            n2 = self.nodes[(n1_index + random.randint(1,node_count-1)) % node_count]
            if not n1.id in n2.neighbours.keys():
                self.add_link(n1,n2)
                extra_links += 1
        """ this seems like the easiest way to do this
            pick a random edge, pick a different random edge
            see if they already have a link
            if they do pick another random pair
            if not then add an edge
            this will start to suck as link_count approaches node_count"""


    def add_link(self, n1, n2):
        cost = random.randint(5,100)/10.0
        n1.neighbours[n2.id] = (cost, n2.port)
        n2.neighbours[n1.id] = (cost, n1.port)
        print(n1.id, n2.id, cost)

def config_files(network, directory = os.path.join(os.getcwd(), "configs")):
    if not os.path.exists(directory):
        os.mkdir(directory)
    for node in network.nodes:
        filename = node.id+"config.txt"
        with open(os.path.join(directory, filename), 'w') as file:
            file.write(str(len(node.neighbours.keys()))+ "\n")
            for neighbour in node.neighbours.keys():
                file.write(neighbour + " ")
                file.write(str(node.neighbours[neighbour][0]) + " ")
                file.write(str(node.neighbours[neighbour][1]) + "\n")

n = Network()
config_files(n)
