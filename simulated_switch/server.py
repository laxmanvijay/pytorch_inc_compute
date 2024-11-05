# open tcp port 10000 and listen for incoming connections
# when a connection is made, read the data and print it
# then close the connection
# repeat

import socket
import sys

from master import SimulatedSwitchMaster

try:
    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = 10000

    # bind to the port
    serversocket.bind(('localhost', port))
    print("Listening on port %d" % port)

    # queue up to 5 requests
    serversocket.listen(5)

    simulated_switch_master = SimulatedSwitchMaster()

    while True:
        try:
            # establish a connection
            clientsocket, addr = serversocket.accept()
            print("Got a connection from %s" % str(addr))

            data = b""
            while True:
                packet = clientsocket.recv(1024)
                if not packet:
                    break
                data += packet
            print("Received: %s" % data)

            result = simulated_switch_master.process(data)
            print("Result: %s" % result)

            clientsocket.send(result)
            clientsocket.close()
        except socket.error as e:
            print("Socket error: %s" % e)
        except socket.timeout as e:
            print("Socket timeout: %s" % e)
        except Exception as e:
            print("Other error: %s" % e)
finally:
    serversocket.close()
    print("Server socket closed")

