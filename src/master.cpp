#include "master.h"
#include "worker.h"

namespace Scheduler {

    int schedule(std::vector<int>& data) {

        int num_threads = 4;
        int elements_per_thread = data.size() / num_threads;
        int total_sum = 0;
        boost::mutex mutex;

        // Create threads and assign them portions of the vector
        std::vector<boost::thread> threads;

        for (int i = 0; i < num_threads; ++i) {
            int start = i * elements_per_thread;
            int end = (i == num_threads - 1) ? data.size() : (i + 1) * elements_per_thread;
            threads.emplace_back(Worker::partial_sum, std::cref(data), start, end, std::ref(total_sum), std::ref(mutex));
        }

        // Join all threads
        for (auto& t : threads) {
            t.join();
        }

        return total_sum;
    }
} // namespace Scheduler