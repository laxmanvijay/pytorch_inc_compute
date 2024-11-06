#include <vector>
#include <fmt/core.h>
#include <numeric>
#include <netinet/tcp.h>
#include <netinet/ip.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

namespace Worker {
    int send_to_switch(std::vector<int>& data);
}