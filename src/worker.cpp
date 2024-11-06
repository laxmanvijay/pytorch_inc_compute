#include "worker.h"

namespace Worker
{
    int send_to_switch(std::vector<int>& data) {
        // Create UDP socket
        int sock = socket(AF_INET, SOCK_DGRAM, 0);
        if (sock < 0) {
            fmt::println("Socket creation failed: {}", strerror(errno));
            return -1;
        }

        // Set destination
        struct sockaddr_in server_addr;
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(10001);
        server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

        // Setup IO vector
        struct iovec iov;
        iov.iov_base = data.data();
        iov.iov_len = data.size() * sizeof(int);

        // Setup message header
        struct msghdr msg;
        memset(&msg, 0, sizeof(msg));
        msg.msg_name = &server_addr;
        msg.msg_namelen = sizeof(server_addr);
        msg.msg_iov = &iov;
        msg.msg_iovlen = 1;

        // Send using sendmsg
        if (sendmsg(sock, &msg, 0) < 0) {
            fmt::println("Send failed: {}", strerror(errno));
            close(sock);
            return -1;
        }

        fmt::println("Data sent successfully");

        // Shutdown sending side to signal end of data
        shutdown(sock, SHUT_WR);

        // Receive response
        char buffer[4096];
        int bytes_received = recv(sock, buffer, sizeof(buffer), 0);
        if (bytes_received < 0) {
            fmt::println("Receive failed: {}", strerror(errno));
            close(sock);
            return -1;
        } else if (bytes_received > 0) {
            // Extract the integer result from the received bytes
            int result;
            memcpy(&result, buffer, sizeof(int));
            fmt::println("Result: {}", result);
            return result;
        }

        close(sock);
        return 0;
    }
} // namespace Worker
