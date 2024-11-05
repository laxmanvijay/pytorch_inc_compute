import socketserver
import struct
import sys
from master import SimulatedSwitchMaster

class SimulatedSwitchHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Got a connection from {self.client_address}")
        data = b""
        
        # Receive data
        while True:
            packet = self.request.recv(1024)
            if not packet:
                break
            data += packet
            
        try:
            # Convert bytes to list of integers
            num_ints = len(data) // 4
            int_data = struct.unpack(f'{num_ints}i', data)
            print("Received data:", list(int_data))
            
            # Process data
            result = self.server.switch_master.process(list(int_data))
            print("Process result:", result)
            
            # Send result back
            if result:
                result_bytes = struct.pack('i', result)
                self.request.send(result_bytes)
                
        except struct.error as e:
            print("Data conversion error:", e)
        except Exception as e:
            print("Processing error:", e)

class SimulatedSwitchServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.switch_master = SimulatedSwitchMaster()
        self.allow_reuse_address = True

def main():
    try:
        port = 10001
        server = SimulatedSwitchServer(('localhost', port), SimulatedSwitchHandler)
        print(f"Listening on port {port}")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        server.server_close()
    except Exception as e:
        print(f"Server error: {e}")
        
if __name__ == "__main__":
    main()

