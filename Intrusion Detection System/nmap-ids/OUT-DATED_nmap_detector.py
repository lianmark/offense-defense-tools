# Tested
# Transparency: approximately 40–50% of this code was AI-assisted.
# Status: Work in progress — some lines/functions may be incomplete or mixed in purpose.
#
# Purpose: Gain familiarity with intrusion detection system (IDS) tools for personal learning,
#          and observe and understand how actual network packets look.
#
# Description: Detects if someone is running Nmap against this machine by monitoring inbound packets.
# Method: Counts inbound packets in a rolling 5-second window; if the count reaches 100 or more,
#         it flags a likely Nmap scan.
#
# Code Published: 09/09/2025
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
            
        
