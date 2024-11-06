#include "master.h"
#include "worker.h"

#define __APPLE_USE_RFC_3542  // for advanced IP-level socket options

namespace Scheduler {

    int schedule(std::vector<int>& data) {
        fmt::println("Scheduling data: {}", data);
        return Worker::send_to_switch(data);
    }
} // namespace Scheduler