#include "worker.h"

namespace Worker
{
    void partial_sum(const std::vector<int>& data, int start, int end, int& total_sum, boost::mutex& mutex) {
        int local_sum = std::accumulate(data.begin() + start, data.begin() + end, 0.0);

        // Lock the mutex before updating the global sum
        boost::lock_guard<boost::mutex> lock(mutex);
        total_sum += local_sum;
    }
} // namespace Worker
