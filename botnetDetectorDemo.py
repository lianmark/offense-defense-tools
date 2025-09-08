# This is an unfinished & unoptimized project – running it may cause high CPU usage and significantly slow down your computer depends on your cpu.
# Since its Demo and unfinished code - code will abort after logs.txt reach more than 50MB to prevent space cost, feel free to change or remove it
# Compatible with Windows 10/11 only. Linux and other operating systems may encounter issues running this code.
# Created by Lian M
# Date Published: 09/08/2025
# This is my first ever complex project.
# For full transparency, around 10–15% of the code was AI-generated, but I fully understand all of it.
# get_ram and get_cpu in the if statement should be modified by user
import psutil as ps   
import win32api 
import time   
import datetime 
import subprocess as sb
import socket
import os
   
initial_create = False 
get_validated = False
total_ip_port = 0
Iterations = 0
procs = {}
passed_initial_iteration = False

username = os.getenv("username")
os.makedirs("C:\\Users\\"+username+"\\Desktop\\Botnet_logs", exist_ok=True)

    
while True:
    
    get_ram = ps.virtual_memory().percent 
    get_cpu = ps.cpu_percent(interval=1)      
    last_input_ms = win32api.GetLastInputInfo()     
    now_ms = win32api.GetTickCount()     
    idle_seconds = (now_ms - last_input_ms) // 1000
      
    if idle_seconds > 2:
        if passed_initial_iteration is True:       
         Iterations = Iterations+1 
        for pid in ps.pids():                          
            if pid not in procs:                               
                try:                     
                    p = ps.Process(pid)
                    p.cpu_percent()  #Baseline                    
                    procs[pid] = p                               
                except (ps.NoSuchProcess, ps.AccessDenied, ps.ZombieProcess):                                        
                    pass          
        time.sleep(2)       
        
        for pid in list(procs.keys()):
            if not ps.pid_exists(pid):
                procs.pop(pid) # removing the current dead pid

        if get_cpu > 2 and get_ram > 2:
            if initial_create is False:
             with open ("C:\\Users\\" +username+ "\\Desktop\\Botnet_logs\\logs.txt", "a") as f:                
                 f.write(str(datetime.datetime.now()) + " Alert: High resource usage detected\nCPU: " + str(get_cpu) + "%  RAM: " +str(get_ram) + "\nAction: Investigation started\n--------------------------------------------------------------------------\n" )
                 initial_create = True
            for pid in procs:               
                try: 
                    connections = procs[pid].connections(kind="inet")
                    remote_ip = None
                    remote_port = None
                    for conn in connections:
                        if conn.raddr:
                            remote_ip = conn.raddr.ip
                            remote_port = conn.raddr.port 
                            try: 
                                service = socket.getservbyport(remote_port)
                                service_str = service.upper() + " (standard port)"
                            except OSError:
                                service_str = "Unknown_Port_ERROR"
                                               
                    current_pid_cpu = procs[pid].cpu_percent(None) 
                    current_pid_ram = procs[pid].memory_info().rss / (1024*1024)                             
                    get_name = procs[pid].name()
                    exe_path = procs[pid].exe()

                     
                    if not exe_path or exe_path.strip() == "":
                        continue  # skip this process only (no exe path), move on to the next pid in the loop
                    if current_pid_cpu > 0 and get_ram >= 1:
                        check = sb.run(["powershell", "-Command", "Get-AuthenticodeSignature '" + exe_path + "'"],
                        capture_output=True, text=True) 
                        check_output = check.stdout
                          
                        if "Valid" in check_output:
                             get_validated = True
                         
                        with open ("C:\\Users\\" +username+ "\\Desktop\\Botnet_logs\\logs.txt", "a") as f:
                         f.write("Iterations:    " + str(Iterations)+ "\n") 
                         f.write("Path:      " + str(os.path.dirname(exe_path)) +"\ \n")
                         f.write("Name:         " + str(get_name) + "\n")
                         f.write("CPU:          " + str(current_pid_cpu) + "%" + "\n")
                         f.write("RAM:          " + str(current_pid_ram) + " MB" + "\n")
                         f.write("Signature:    " + str(get_validated) + "\n")  
                         if remote_ip not in ("127.0.0.1", "::1") and remote_port is not None and remote_ip is not None:
                          total_ip_port = total_ip_port+1
                          f.write("Connected to: " + str(remote_ip) + " : " + str(remote_port) +" -> "+ service_str + "\n")
                          f.write("Number of Unique IP:Port Connections Detected: "+ str(total_ip_port) +"\n")
                         f.write("--------------------------------------------------------------------------\n\n\n\n")
                         
                         log_file_size = os.path.getsize("C:\\Users\\"+username+"\\Desktop\\Botnet_logs\logs.txt")
                         if log_file_size / (1024 * 1024) > 50:
                             break
                         
                           
                    get_validated = False     

                except (ps.NoSuchProcess, ps.AccessDenied, ps.ZombieProcess):                                 
                    pass
        passed_initial_iteration = True      
            
    else:         
        procs.clear()  
        time.sleep(1)       
