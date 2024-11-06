# test_allreduce.py
import unittest
from unittest.mock import Mock, patch
import multiprocessing
import socket
import struct
from master import SimulatedSwitchMaster
from worker import SimulatedSwitchWorker

class TestAllReduce(unittest.TestCase):
    def setUp(self):
        self.master = SimulatedSwitchMaster()
        
    def test_worker_process(self):
        # Test single worker processing
        test_data = [1, 2, 3, 4]
        queue = multiprocessing.Queue()
        
        worker = SimulatedSwitchWorker()
        worker.process(test_data, queue)
        
        result = queue.get()
        self.assertEqual(result, 10)  # sum of [1,2,3,4]

    def test_end_to_end(self):
        # Test complete allreduce operation
        test_data = [1, 2, 3, 4]
        num_workers = 2
        
        queue = multiprocessing.Queue()
        processes = []
        
        # Create and start worker processes
        for _ in range(num_workers):
            worker = SimulatedSwitchWorker()
            p = multiprocessing.Process(
                target=worker.process, 
                args=(test_data, queue)
            )
            processes.append(p)
            p.start()
            
        # Wait for processes to complete
        for p in processes:
            p.join()
            
        # Collect results
        results = []
        while not queue.empty():
            results.append(queue.get())
            
        # Verify final sum
        final_sum = sum(results)
        self.assertEqual(final_sum, 20)  # 2 workers * sum([1,2,3,4])

    @patch('socket.socket')
    def test_schedule(self, mock_socket):
        # Setup mock socket and response
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        
        # Mock receive data (simulating server response of sum=10)
        mock_sock.recv.return_value = struct.pack('i', 10)
        
        # Test data
        test_data = [1, 2, 3, 4]
        
        # Create master instance
        master = SimulatedSwitchMaster()
        
        # Call schedule method
        result = master.process(test_data)
        
        # Verify result
        self.assertEqual(result, 10)

if __name__ == '__main__':
    unittest.main()