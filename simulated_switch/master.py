import scapy.all as scapy
import multiprocessing

from worker import SimulatedSwitchWorker

class SimulatedSwitchMaster:
    def process(self, data):
        print("Processing data: %s" % data)
        # parse the incoming tcp packet using scapy
        packet = scapy.IP(data)
        
        print(packet.show())
        payload = packet[scapy.TCP].payload

        print(payload)
        tcp_headers = packet[scapy.TCP].fields
        print(tcp_headers)

        workers = [SimulatedSwitchWorker() for i in range(tcp_headers['data_size'])]

        result_queue = multiprocessing.Queue()

        # Start a process for each worker
        processes = []
        chunk_size = len(payload) // len(workers)
        for i, worker in enumerate(workers):
            start = i * chunk_size
            end = start + chunk_size if i < len(workers)-1 else len(payload)
            p = multiprocessing.Process(target=worker.process, 
                                      args=(payload[start:end], result_queue))
            processes.append(p)
            p.start()

        # Wait for all processes to finish
        for p in processes:
            p.join()

        # Collect all results from the queue
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())

        # Perform the reduction operation (sum in this case)
        total_sum = sum(results)

        # Return the results
        return total_sum