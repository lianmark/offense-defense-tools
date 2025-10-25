## Note: This is a small, unfinished project and may still contain bugs under certain conditions.
## All IPs that communicate with this PC are saved in a JSON file and monitored by this program.
## If an IP sends more than 100 packets within 5 seconds, an alert will be shown.
##
## Transparency: I used ChatGPT (an AI assistant) for guidance and suggestions.
## I wrote and assembled the code myself — ChatGPT only provided snippets and advice, not a full solution.
## I currently understand approximately 80–90% of the code and its functionality.
##
## Published on 09/21/2025 by Lian Mark

import psutil as ps
from scapy.all import *
import pydivert as pd 
import time
import json
import os 

connections = ps.net_connections(kind='inet')
list_active_connections = []   
translate_protocol = "ERROR_PROTOCOL_NAME"
per_ip = {}
SUSPECTED_IPS_PATH = r"C:\Users\PC\Desktop\nscs-system\Anti-virus\connection_logs.json"

if not os.path.exists(SUSPECTED_IPS_PATH):
    with open(SUSPECTED_IPS_PATH, "w") as f:
        json.dump({}, f)
else:
    with open(SUSPECTED_IPS_PATH, "r", encoding="utf-8") as f:
        per_ip = json.load(f)
        
    for ip in per_ip:
        per_ip[ip]["Packets_send_WindowStart"] = None
        per_ip[ip]["LastSeen"] = None
    with open(SUSPECTED_IPS_PATH, "w", encoding="utf-8") as f:
        json.dump(per_ip, f, indent=4)
        
def start_monitor():
    try:
        with pd.WinDivert("tcp.Syn") as capture:
            for packet in capture:
                NOW_TIME = time.time()
                
                if packet.tcp.syn:
                    first_seen = time.time()
                    ip = packet.src_addr
                    try:
                        with open(SUSPECTED_IPS_PATH, "r", encoding="utf-8") as f:
                            per_ip = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError):
                        per_ip = {}
                    if ip not in per_ip:
                        per_ip[ip] = {
                            "IP": ip,
                            "FirstSeen": first_seen,
                            "Packets_send_over_all": 1,
                            "Packets_send_WindowStart": 0,
                            "LastSeen": NOW_TIME,
                            "WindowStart": NOW_TIME
                        }  
                    else:
                        per_ip[ip]["Packets_send_over_all"] += 1
                        
                        if NOW_TIME - per_ip[ip]["WindowStart"] > 5:
                            per_ip[ip]["WindowStart"] = NOW_TIME
                            per_ip[ip]["Packets_send_WindowStart"] = 1
                            
                        else:
                            per_ip[ip]["Packets_send_WindowStart"] += 1
                    per_ip[ip]["LastSeen"] = NOW_TIME
                    with open(SUSPECTED_IPS_PATH, "w", encoding="utf-8") as f:
                        json.dump(per_ip, f, indent=4)
                window_count = per_ip.get(ip, {}).get("Packets_send_WindowStart", 0) 
                window_time = per_ip.get(ip, {}).get("WindowStart", NOW_TIME)
                
                if window_count > 100 and NOW_TIME - window_time <= 5:
                    for i in range(30):
                        print("ALERT: Possible SYN Flood Attack Detected by!", ip)
                capture.send(packet)
    except Exception as e:
        # Handle WinDivert cleanup errors gracefully
        if "The handle is invalid" not in str(e):
            print(f"Monitor error: {e}")

start_monitor()
