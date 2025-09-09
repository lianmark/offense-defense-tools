import psutil as ps
import os
import datetime 
import socket

get_ip = None
get_port = None
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
private_ip = s.getsockname()[0]
source_port = s.getsockname()[1]
s.close()



username = os.getenv("username")


connections = ps.net_connections(kind="inet")
for con in connections:
    if con.raddr:
        print(con)
        try:
            process = ps.Process(con.pid)
            process_name = process.name()
            
        except ps.NoSuchProcess:
            continue 
        get_ip = con.raddr.ip
        get_port = con.raddr.port
        get_status = con.status
        if get_ip not in ("127.0.0.1", "::1"):
            with open ("C:\\Users\\" +username+ "\\Desktop\\Artificial_Intelligence_Python_Lessons\\Projects\\Intrusion Detection System\\logs.txt", "a") as f:
                f.write("[" + str(datetime.datetime.now()) + "]\n")
                f.write("Source: " + str(private_ip) +" "+ str(source_port)+ "\n")
                f.write("Destination: " + str(get_ip) + " " + str(get_port)+ "\n")
                f.write("Process: "+ str(process_name)+ "\n")
                f.write("Status: " + str(get_status)+ "\n\n\n\n")
