The network topology used in our report is already saved in the config/ folder. however a user can generate a new network topology by simply running:
  `$ python3 network_topology.py`
This new topology will be used the next time that the network is started up.

Each node is created from a separate terminal by running:
  `$ python3 COMP3221_A1_Routing.py <node id> <node port> <node config file>`
note that if the port is not the one expected for that node id as outlined in the assignment specs, an assertion error will happen.
Also note that config file names are of the format `"<node_id>config.txt` The node id is a capital letter, and no slashes are needed before the config file name. The program already knows to look in the config folder.

A full network of 10 nodes must be started by opening 10 terminal windows and running the appropriate commands to start up each node.

The output into each terminal window will contain only information pertaining to the node started by that terminal.

An additional terminal window will be needed if the user wishes to make changes to the network while it's live. for example to change a link cost or simulate a node failure.

This is done by running:

  `$ python3 editor.py`
  `$ FAIL <node id>`
To fail a node
Or
  `$ python3 editor.py`
  `$ RECOVER <node id>`
to recover a failed node.
Or:
  `$ python3 editor.py`
  `$ CHANGE <node1 id> <node2 id>`
To change a link cost between node 1 and node 2.

NO PACKAGES ARE NEEDED TO BE INSTALLED. 
