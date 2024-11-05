# test_allreduce.py
import unittest
from unittest.mock import Mock, patch
import multiprocessing
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
        
    @patch('scapy.all.IP')
    def test_master_allreduce(self, mock_ip):
        # Mock TCP packet data
        test_payload = [1, 2, 3, 4]
        mock_tcp = Mock()
        mock_tcp.payload = test_payload
        
        # Mock TCP headers
        mock_fields = {'data_size': 3}  # Create 3 workers
        mock_tcp.fields = mock_fields
        
        # Setup mock IP packet
        mock_packet = Mock()
        mock_packet.show = Mock(return_value=None)
        mock_packet.__getitem__ = Mock(return_value=mock_tcp)
        mock_ip.return_value = mock_packet
        
        # Test master process
        result = self.master.process(b"mock_data")
        
        # Each worker processes a portion of [1,2,3,4]
        # Final allreduce sum should be 10
        self.assertEqual(result, 10)
        
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

if __name__ == '__main__':
    unittest.main()