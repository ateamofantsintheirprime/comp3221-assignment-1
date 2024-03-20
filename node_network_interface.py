from node import Node
from packet import Packet
import threading, time, socket
ip = 'localhost'

## TODO!! MAKE IT SO THAT THE LISTENING THREAD STORES RECEIVED PACKETS IN A QUEUE
## AND ONLY INTERACTS WITH THE NODE OBJECT ONCE THE SENDING THREAD HAS UNLOCKED IT
## SO WE DONT GET RACE CONDITIONS ALSO MAKE SURE TO CHECK HOW LONG THIS QUEUE IS
## GETTING INCASE CERTAIN NODES ARE GETTING OVERLOADED

## ADD THREAD LOCKING!!!!!!!!
## TRY NOT TO LOCK THE WHOLE NODE IF POSSIBLE, JUST ADD LOCKS TO THE
## VARIABLES THAT ARE GONNA BE ACCESSED BY / INFLUENCE MULTIPLE THREADS

## also figure out how to gracefully close the program


## also note that at the start, each node only knows its neighbours
## so it will need to be adding new nodes to its reachability matrix
## based on the reachability matrices stored in the packets it receives

## rename rechability matrix to link cost matrix
## the shortest path list is where the total path cost and shit is found


## also we cannot assume that every node in the config will exist / be responding
## to us because we cannot open all terminal windows simultaneously

# okay so there are no in transit packages

class NodeNetworkInterface():
    def __init__(self, id, listening_port, config_file):
        # The listening thread should read the destination of
        # each packet it receives, if that destination is this node
        # it should read the packet and process the data
        # if the destination is another node, it should send it to
        # the first node in the shortest path to reach that destiation
        # from this node
        self.config_file = config_file
        # self.id = id
        self.listening_port = listening_port
        self.sending_ports = {}
        self.packet_count = 0
        self.node = Node(id)

        # dont forget to make it periodically re-check the config file to
        # detect changes made through cli
        self.load_from_config()
        self.start_threads()

    def load_from_config(self):
        with open(self.config_file, 'r') as f:
            lines = f.readlines() # it should be open for the minimum amount of time
        for line in lines[1:]: # ignore the first line
            line = line.strip().split(" ")
            n_id = line[0]
            n_cost = float(line[1])
            n_port = int(line[2])
            # may add a line into the config to
            # specify if the node is up or down
            self.sending_ports[n_id] = n_port
            self.node.set_neighbour_costs(n_id, n_cost)

    def start_threads(self):
        listening_thread = threading.Thread(target=self.listen)
        sending_thread = threading.Thread(target=self.broadcast)
        routing_calculations_thread = threading.Thread(target=self.routing_calculations)

        listening_thread.start()
        sending_thread.start()
        routing_calculations_thread.start()

        listening_thread.join()
        sending_thread.join()
        routing_calculations_thread.join()


    def listen(self):
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listening_socket.bind((ip, self.listening_port))
        self.listening_loop(listening_socket)

    def listening_loop(self, listening_socket):
        while True:
            data, addr = listening_socket.recvfrom(1024)
            packet = Packet()
            packet.from_bits(data)
            t = time.strftime("%H:%M:%S.%f")
            print("received packet: ", packet.id, " at time: ", t)
            self.node.read_packet(packet)

    def broadcast(self):
        sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sending_loop(sending_socket)

    def sending_loop(self, sending_socket):
        packet_send_time = time.time() + 10
        while True:
            current_time = time.time()
            if current_time >= packet_send_time:
                packet_send_time = current_time + 10
                print("broadcasting...")
                self.send_packets(sending_socket)

            elif current_time + 9 <= packet_send_time:
                time.sleep(8)
                # i dont trust that sleep(8) wont have some imprecision
                # that compounds as the program runs over time
                # this makes it so the loop isnt spamming so hard
                # when the packet send time is still several seconds away

    def send_packets(self, sending_socket):
        for n_id in self.node.get_neighbour_ids():
            destination_port = self.sending_ports[n_id]
            packet = Packet()
            packet.data = self.node.get_reachability_matrix()
            packet.source = self.node.id
            packet.id = self.packet_count

            t = time.strftime("%H:%M:%S.%f")
            print("sending: ", packet.id, " time: ",t )
            sending_socket.sendto(packet.to_bits(), (ip, destination_port))
            self.packet_count += 1

    def routing_calculations(self):
        time.sleep(60)
        self.routing_calculations_loop()

    def routing_calculations_loop(self):
        while True: # gotta be a better way to do this than while true
            if self.node.recalculate_routing_trigger:
                self.node.recalculate_routing_trigger = False
                self.node.calculate_shortest_paths()
            time.sleep(0.1) # dont want this shit to spam too hard
