import serial.tools.list_ports
import tkinter as tk
import time
from dronekit import connect


#vehicle = connect('COM8', wait_ready=True,baud=115200)

def connect_init():
    global windows, connect_btn, refresh_btn
    windows = tk.Tk()
    windows.title("大頭")
    windows.geometry("800x600")
    windows.config(bg="white")
    
    port_lable = tk.Label(windows, text="Available Port(s): ", bg="white")
    port_lable.grid(column=1, row=2, pady=20, padx=10)

    port_bd = tk.Label(windows, text="Baude Rate: ", bg="white", )
    port_bd.grid(column=1, row=3, pady=20, padx=10)
    
    refresh_btn = tk.Button(windows, text = "R", height = 2, 
                            width = 10,command= update_coms)
    refresh_btn.grid(column=3, row=2)
    
    connect_btn = tk.Button(windows, text = "Connect", height = 2, width = 10,
                            state="disabled", command = connextion)
    connect_btn.grid(column=3, row=4)
    
    update_coms()
    baud_select()

def connect_check(args):
    
    if "-" in clicked_bd.get() or "-" in clicked_com.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"
    
def baud_select():
    global clicked_bd, drop_bd
    clicked_bd = tk.StringVar()
    bds = ["-",
           "300",
           "600",
           "1200",
           "2400",
           "4800",
           "9600",
           "14400",
           "19200",
           "28800",
           "38400",
           "56000",
           "57600",
           "115200",
           "128000",
           "256000"]
    clicked_bd.set(bds[13])
    drop_bd = tk.OptionMenu(windows, clicked_bd, *bds, command=connect_check)
    drop_bd.config(width=20)
    drop_bd.grid(column=2, row=3, padx=50)
    
    
def update_coms():
    global drop_com, clicked_com,ports
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    
    clicked_com = tk.StringVar()
    clicked_com.set(coms[0])
    drop_com = tk.OptionMenu(windows, clicked_com, *coms, command=connect_check)
    drop_com.config(width=20)
    drop_com.grid(column=2, row=2, padx=50)


def connextion():
    global serialData,ser,connect_btn
    if connect_btn["text"] in "Connect":
        serialData = True
        connect_btn["text"] = "Disconnect"
        refresh_btn["state"] = "disable"
        drop_bd["state"] = "disable"
        drop_com["state"] = "disable"
        port = clicked_com.get()
        baud = clicked_bd.get()
        
        try:
           ser = serial.Serial(port, baud, timeout=0)
        except:
            pass

    else:
        serialData = False
        connect_btn["text"] = "Connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_com["state"] = "active"

#ports = serial.tools.list_ports.comports()
#print(ports)
connect_init()

#windows.protocol("WM_DELETE_WINDOW",close_window)
windows.mainloop()