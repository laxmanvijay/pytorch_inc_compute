from scapy.all import IP, TCP, Raw
import multiprocessing

from worker import SimulatedSwitchWorker

class SimulatedSwitchMaster:
    def process(self, data):
        print("Processing data length: %d" % len(data))
        try:
            # Create workers based on data size
            num_workers = min(4, len(data))  # Max 4 workers
            workers = [SimulatedSwitchWorker() for _ in range(num_workers)]
            result_queue = multiprocessing.Queue()

            processes = []
            if data:
                chunk_size = len(data) // len(workers)
                for i, worker in enumerate(workers):
                    start = i * chunk_size
                    end = start + chunk_size if i < len(workers)-1 else len(data)
                    p = multiprocessing.Process(target=worker.process, 
                                              args=(data[start:end], result_queue))
                    processes.append(p)
                    p.start()

            # Wait for all processes to complete
            for p in processes:
                p.join()

            # Collect results
            results = []
            while not result_queue.empty():
                results.append(result_queue.get())

            return sum(results)

        except Exception as e:
            print(f"Error processing data: {str(e)}")
            return None