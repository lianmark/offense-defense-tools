# ================================================================
#  Nmap + DDoS Detector (IDS Prototype)
#  Published: 2025-09-10
#  Contribution: ~60% of the logic and structure was CO-CREATED 
#                with AI guidance (assistant).
#  NOTE: The AI assistant did NOT provide a single, finished script.
#        I wrote/assembled this program myself and iterated on it;
#        the AI only provided guidance, snippets, and debugging tips
#  WARNING: This code may consume significant CPU due to the 
#           continuous capture loop and high iteration counts.
# ================================================================
################# Known bugs:
# - Firewall won't block hacker's connection (in and out bound)
import psutil as ps
from scapy.all import *
import pydivert as pd 
import time
import subprocess


capture_uniqe_ip = "0.0.0.0"
connections = ps.net_connections(kind='inet')
list_active_connections = []   
translate_protocol = "ERROR_PROTOCOL_NAME"
PORTS_SCANNED = []
IP_CAPTURED = []
CAPTURED_ATTACKERS = {}
STOP_CAPTURE = False

username = os.getenv("username")
os.makedirs("C:\\Users\\"+username+"\\Desktop\\\Artificial_Intelligence_Python_Lessons\\Projects\\Intrusion Detection System\\", exist_ok=True)

def check_existing_connections(connections):
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
                global capture_uniqe_ip
                capture_uniqe_ip = "ip.SrcAddr == " + str(con.raddr.ip)    

check_existing_connections(connections)
print("Monitoring network... Wll alert on suspicious activity!")

START_TIME = time.time()

with pd.WinDivert("(tcp or udp) and inbound") as capture:
    for packet in capture:
        if STOP_CAPTURE:
            break
    
        if packet.tcp:
            TCP_NOW_TIME = time.time()
            print(packet.src_addr,":",packet.src_port, " -> ", packet.dst_addr,":", packet.tcp.dst_port , " ", translate_protocol, " -> ", "[SYN] Seq=",packet.tcp.seq_num, " Ack=", packet.tcp.ack_num)
            global TCP_SRC
            TCP_SRC = packet.src_addr
            dst_port = packet.tcp.dst_port # port being scanned
            if TCP_SRC not in CAPTURED_ATTACKERS:
                CAPTURED_ATTACKERS[TCP_SRC] = {"ports": set(), "count": 0, "start_time": time.time(), "attacker_ip": TCP_SRC}
        
            if packet.tcp.syn:
                CAPTURED_ATTACKERS[TCP_SRC]["ports"].add(dst_port)
                CAPTURED_ATTACKERS[TCP_SRC]["count"] += 1          
            # Nmap-scan capture logic
            if  (TCP_NOW_TIME - CAPTURED_ATTACKERS[TCP_SRC]["start_time"]) >=5 and len(CAPTURED_ATTACKERS[TCP_SRC]["ports"]) > 100:
                    print("\n\n\nALERT: Possible SYN Flood Attack Detected!\n")
                    print("Possible Nmap-Scan is being prepormed on your system to gather information about open ports and services running on your system.\n")
                    print("Source IP:", CAPTURED_ATTACKERS[TCP_SRC])
                    STOP_CAPTURE = True
        
        if packet.udp:
            UDP_NOW_TIME = time.time()
            global UDP_SRC
            UDP_SRC = packet.src_addr
            dst_port = packet.udp.dst_port # port being scanned
            if UDP_SRC not in CAPTURED_ATTACKERS:
                CAPTURED_ATTACKERS[UDP_SRC] = {"ports": set(), "count": 0, "start_time": time.time(), "attacker_ip": UDP_SRC}
            print(packet.src_addr, ":", packet.src_port, " -> ",packet.dst_addr, ":", packet.udp.dst_port," Payload size=", len(packet.udp.payload))
            payload_size = len(packet.udp.payload)
            if payload_size == 1490 or payload_size > 1000:
                CAPTURED_ATTACKERS[UDP_SRC]["ports"].add(dst_port)
                CAPTURED_ATTACKERS[UDP_SRC]["count"] += 1  
        # Ddos-flood capture logic
            if  (UDP_NOW_TIME - CAPTURED_ATTACKERS[UDP_SRC]["start_time"]) >= 5 and CAPTURED_ATTACKERS[UDP_SRC]["count"] > 1500:
                print("\n\nALERT: Possible DDoS Flood Attack Detected!\n")
                print("DDoS attack is being prepormed on your system to overwhelm your network or system resources, making it unavailable to legitimate users.\n")
                print("Source IP:", CAPTURED_ATTACKERS[UDP_SRC])
                with open ("C:\\Users\\" +username+ "\\Desktop\\\Artificial_Intelligence_Python_Lessons\\Projects\\Intrusion Detection System\\IDS-logs.txt", "a") as f:                
                    f.write("\n\n\nSource IP:" + str(CAPTURED_ATTACKERS[UDP_SRC]))
                    block = "8.8.8.8"
                subprocess.run([
                    "powershell",
                    "-Command",
                    "netsh advfirewall firewall add rule name=\"Block_"+CAPTURED_ATTACKERS[UDP_SRC]["attacker_ip"]+"\" dir=out action=block remoteip=" + blCAPTURED_ATTACKERS[UDP_SRC]["attacker_ip"]
                    ])
                subprocess.run([
                    "powershell",
                    "-Command",
                    "netsh advfirewall firewall add rule name=\"Block_"+CAPTURED_ATTACKERS[UDP_SRC]["attacker_ip"]+"\" dir=in action=block remoteip=" + CAPTURED_ATTACKERS[UDP_SRC]["attacker_ip"]
                    ])
                print(CAPTURED_ATTACKERS[UDP_SRC]["attacker_ip"])
                STOP_CAPTURE = True 


