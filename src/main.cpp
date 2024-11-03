// This is not used in CmakeLists.txt (commented out)
// Only for testing purposes.

#include "master.h"
#include <fmt/core.h>
#include <vector>

int main() {
    std::vector<int> data; 

    for (int i = 0; i < 40; i++) {
        data.push_back(i);
    }

    int res = Scheduler::schedule(data);
    fmt::print("Result: {}\n", res);
    return 0;
}