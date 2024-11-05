#include <iostream>
#include <vector>
#include <cstring>
#include <netinet/tcp.h>
#include <netinet/ip.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include "master.h"
#include "worker.h"
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#define __APPLE_USE_RFC_3542  // for advanced IP-level socket options

namespace Scheduler {

    struct pseudo_header {
        u_int32_t source_address;
        u_int32_t dest_address;
        u_int8_t placeholder;
        u_int8_t protocol;
        u_int16_t tcp_length;
    };

    int schedule(std::vector<int>& data) {
        // Create TCP socket instead of raw socket
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            std::cerr << "Socket creation failed: " << strerror(errno) << std::endl;
            return -1;
        }

        // Set destination
        struct sockaddr_in server_addr;
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(10001);
        server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

        // Connect to server
        if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
            std::cerr << "Connection failed: " << strerror(errno) << std::endl;
            close(sock);
            return -1;
        }

        // Send data directly
        size_t total_size = data.size() * sizeof(int);
        if (send(sock, data.data(), total_size, 0) < 0) {
            std::cerr << "Send failed: " << strerror(errno) << std::endl;
            close(sock);
            return -1;
        }

        std::cout << "Data sent successfully" << std::endl;

        // Shutdown sending side to signal end of data
        shutdown(sock, SHUT_WR);

        // Receive response
        char buffer[4096];
        int bytes_received = recv(sock, buffer, sizeof(buffer), 0);
        if (bytes_received < 0) {
            std::cerr << "Receive failed: " << strerror(errno) << std::endl;
            close(sock);
            return -1;
        } else if (bytes_received > 0) {
            // Extract the integer result from the received bytes
            int result;
            memcpy(&result, buffer, sizeof(int));
            std::cout << "Received result: " << result << std::endl;
            return result;
        }

        close(sock);
        return 0;
    }
} // namespace Scheduler