# Note: This code is unfinished. Some lines and functions may be incomplete or mixed in purpose.  
# For full transparency – this code is approximately 40–50% AI-generated.  
# Purpose: to gain familiarity with intrusion detection system (IDS) tools for personal learning and experience, additionally to observe and understand how actual network packets look.  
# Code Published: 09/09/2025  
# Description: This code detects if someone is running Nmap against your machine.  
# Method: It captures inbound packets and checks whether the number of packets 
# within a 5-second window is 100 or more, which strongly indicates an Nmap scan.  
import psutil as ps
from scapy.all import *
import pydivert as pd 
import time



capture_uniqe_ip = "0.0.0.0"
connections = ps.net_connections(kind='inet')
list_active_connections = []   
translate_protocol = "ERROR_PROTOCOL_NAME"

for con in connections:
    if con.raddr:
        try:
            proc_name = ps.Process(con.pid).name()
        except (ps.NoSuchProcess, ps.ZombieProcess):
            proc_name = "N/A"
        list_active_connections.append({
            "process_id": con.pid,
            "process_name": proc_name,
            "dest_port": con.raddr.port,
            "dest_ip": con.raddr.ip
        })
        if proc_name != "N/A" and con.raddr.ip != "127.0.0.1" and "::1":
            capture_uniqe_ip = "ip.SrcAddr == " + str(con.raddr.ip)

print("Monitoring network... will alert on suspicious activity!")

for i in list_active_connections:
    pass
START_TIME = time.time()
NUMBER_OF_PACKETS_TO_CAPTURE = 0
START_TIMER = False
with pd.WinDivert("tcp.Syn and inbound") as capture:
    for packet in capture:
        NOW_TIME = time.time()
        # if packet.tcp:
        #     translate_protocol = "TCP"
        # if packet.udp:
        #     translate_protocol = "UDP" 
        # if packet.tcp.syn:       
        #     print(packet.src_addr,":",packet.src_port, " -> ", packet.dst_addr,":", packet.tcp.dst_port , " ", translate_protocol, " -> ", "[SYN] Seq=",packet.tcp.seq_num, " Ack=", packet.tcp.ack_num)
        if packet.tcp.syn:
            NUMBER_OF_PACKETS_TO_CAPTURE += 1
        if NUMBER_OF_PACKETS_TO_CAPTURE > 100 and NOW_TIME - START_TIME >=5:
                print("ALERT: Possible SYN Flood Attack Detected!")
                print("Source IP:", packet.src_addr)
                break 
            
        
