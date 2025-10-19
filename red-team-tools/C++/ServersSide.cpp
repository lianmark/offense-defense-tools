#include <iostream>
#include <winsock2.h>   // main socket API: socket(), connect(), send(), recv(), closesocket()
#include <ws2tcpip.h>   // modern helpers: getaddrinfo(), inet_ntop(), inet_p
#include <fstream>
using namespace std;

int main() {


    cout << "test";
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    int typeIP = AF_INET;
    int typeCOM = SOCK_STREAM;
    int protocol = 0;
    SOCKET serverSocket = socket(typeIP, typeCOM, protocol);

    if (serverSocket == INVALID_SOCKET) {
        cout << "error: INVALID SOCKET";
    }
    sockaddr_in serverAddr{};
    serverAddr.sin_family = typeIP;
    serverAddr.sin_port = htons(8080);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    char sendBuffer[1024] = {0};
    cout << "Enter A command" << endl;
    cin.getline(sendBuffer, sizeof(sendBuffer));

    bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));
    listen(serverSocket, SOMAXCONN);
    SOCKET clientSocket = accept(serverSocket,NULL, NULL);

    ofstream myfile;
    myfile.open("example.txt");

    send(clientSocket, sendBuffer, (int)strlen(sendBuffer) + 1, 0);

    char buffer[1024];
    int rec;
    while ((rec = recv(clientSocket, buffer, sizeof(buffer) - 1, 0)) > 0) {
        buffer[rec] = '\0';
        myfile << buffer;
        cout << buffer;
    }
    myfile.close();
    closesocket(clientSocket);
    closesocket(serverSocket);
    WSACleanup();
    return 0;
}
