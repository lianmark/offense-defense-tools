#fully-made by Chat-GPT

import tkinter as tk
import subprocess

def run_script():
    # change path to your NSCSMain.py
    subprocess.Popen(["python", r"C:\Users\PC\Desktop\nscs-system\Anti-virus\NSCSMain.py"])

root = tk.Tk()
root.title("NSCS Systems")

root.state("zoomed")

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True)
# draw circle (oval)
circle = canvas.create_oval(255, 255, 455, 455, fill="red")

# bind mouse click to run_script
canvas.tag_bind(circle, "<Button-1>", lambda e: run_script())

root.mainloop()
