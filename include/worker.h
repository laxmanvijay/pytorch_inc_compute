#include <boost/thread.hpp>
#include <boost/thread/mutex.hpp>
#include <vector>
#include <numeric>

namespace Worker {
    void partial_sum(const std::vector<int>& data, int start, int end, int& total_sum, boost::mutex& mutex);
}