class SimulatedSwitchWorker:
    def process(self, data, result_queue):
        print("Processing data: %s" % data)
        # do something with the data
        result = sum(data)
        result_queue.put(result)