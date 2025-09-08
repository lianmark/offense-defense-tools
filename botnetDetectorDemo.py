import psutil as ps   
import win32api 
import time   
import datetime 
import subprocess as sb
import hashlib

initial_create = False 
last_action = datetime.datetime.now() 
procs = {}
get_validated = False
 

while True:
    current_time = datetime.datetime.now()
    get_ram = ps.virtual_memory().percent 
    get_cpu = ps.cpu_percent(interval=1)      
    last_input_ms = win32api.GetLastInputInfo()     
    now_ms = win32api.GetTickCount()     
    idle_seconds = (now_ms - last_input_ms) // 1000           
    
    if idle_seconds > 2:
        print("Monitoring...")
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

        if get_cpu > 2 or get_ram > 2:
            with open (r"C:\Users\PC\Desktop\Artificial_Intelligence_Python_Lessons\Projects\logs.txt", "a") as f:                
                f.write(str(datetime.datetime.now()) + " Alert: High resource usage detected\nCPU: " + str(get_cpu) + "%  RAM: " +str(get_ram) + "\nAction: Investigation started\n--------------------------------------------------------------------------\n" )
            
            for pid in procs:               
                try: 
                    connections = procs[pid].connections(kind="inet")
                    remote_ip = None
                    remote_port = None
                    for conn in connections:
                        if conn.raddr:
                            remote_ip = conn.raddr.ip
                            remote_port = conn.raddr.port                
                    current_pid_cpu = procs[pid].cpu_percent(None) 
                    current_pid_ram = procs[pid].memory_info().rss / (1024*1024)                             
                    get_name = procs[pid].name()
                    exe_path = procs[pid].exe()

                     
                    if not exe_path or exe_path.strip() == "":
                        continue  # skip this process only (no exe path), move on to the next pid in the loop
                    # print("we here")
                    # print("we here0.5")
                    if current_pid_cpu > 0 and get_ram >= 1:
                        print("we here2")
                        check = sb.run(["powershell", "-Command", "Get-AuthenticodeSignature '" + exe_path + "'"],
                        capture_output=True, text=True) 
                        check_output = check.stdout
                          
                        if "Valid" in check_output:
                             get_validated = True
                         
                        with open (r"C:\Users\PC\Desktop\Artificial_Intelligence_Python_Lessons\Projects\logs.txt", "a") as f:
                         print("we here3")
                         f.write("Process:      " + str(exe_path) + "\n")
                         f.write("CPU:          " + str(current_pid_cpu) + "%" + "\n")
                         f.write("RAM:          " + str(current_pid_ram) + " MB" + "\n")
                         f.write("Signature:    " + str(get_validated) + "\n")  
                         if remote_ip not in ("127.0.0.1", "::1") and remote_port is not None and remote_ip is not None:
                          f.write("Connected to: " + str(remote_ip) + ": " + str(remote_port) + "\n")
                         f.write("--------------------------------------------------------------------------\n")    
                    get_validated = False     

                except (ps.NoSuchProcess, ps.AccessDenied, ps.ZombieProcess):                                 
                    pass 
            
    else:
        print("Not idle...")          
        procs.clear()  
        time.sleep(1)       
        # print("Stopping Monitor Mode, User Is Not Idle!")
        if get_cpu > 40 or get_ram > 58:
            break
