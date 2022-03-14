from __future__ import print_function
import tkinter as tk
from dronekit import connect, VehicleMode
import time



vehicle = connect('udp:127.0.0.1:14550', wait_ready=True, baud=115200) #與飛機連線

# 第1步，例項化object，建立視窗window
window = tk.Tk()

# 第2步，給視窗的視覺化起名字
window.title('My Window')

# 第3步，設定視窗的大小(長 * 寬)
window.geometry('500x300')  # 這裡的乘是小x

# 第4步，在圖形介面上設定標籤
var = tk.StringVar()    # 將label標籤的內容設定為字元型別，用var來接收hit_me函式的傳出內容用以顯示在標籤上
l = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
# 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
l.pack()

# 定義一個函式功能（內容自己自由編寫），供點選Button按鍵時呼叫，呼叫命令引數command=函式名
on_hit = False
on_mode = False
on_take = False

e = tk.Entry(window,show = None)#顯示成明文形式
e.insert(0, "0")
e.pack()
#設定自動起飛
def arm_and_takeoff():
    global on_take
    if on_take == False:
        on_take =True
        
        """
        Arms vehicle and fly to aTargetAltitude.
        """
    
        print ("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        while not vehicle.is_armable:
            print (" Waiting for vehicle to initialise...")
            time.sleep(1)
    
        print ("Arming motors")
        # Copter should arm in GUIDED mode
        vehicle.mode    = VehicleMode("GUIDED")
        vehicle.armed   = True
    
        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            print (" Waiting for arming...")
            time.sleep(1)
    
        print ("Taking off!")
        vehicle.simple_takeoff(float(e.get())) # Take off to target altitude
        var.set('takeoff')
        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #  after Vehicle.simple_takeoff will execute immediately).
    else:
        on_take = False
        var.set('')

#設定模式選單
def mode_select():
    global clicked_mode, drop_mode
    clicked_mode = tk.StringVar()
    bds = ["STABILIZE",
           "ALT_HOLD",
           "AUTO",
           "GUIDED",
           "LOITER",
           "RTL",
           "LAND",]
    clicked_mode.set(bds[0])
    drop_mode = tk.OptionMenu(window, clicked_mode, *bds)
    drop_mode['menu'].config(fg = "green")
    drop_mode.config(width=20)
    drop_mode.pack()

def connect():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('you hit me')
    else:
        on_hit = False
        var.set('')
#設定RTL模式
def rtl():
    global on_mode
    if on_mode == False:
        on_mode = True
        
        vehicle.mode = VehicleMode("RTL")
        var.set('RTL')
    elif vehicle.mode.name != "RTL":
        on_mode = False
        RTL["state"] = "normal"
        var.set('')
def mode():
    print(clicked_mode.get())
    vehicle.mode = VehicleMode(clicked_mode.get())
    var.set(clicked_mode.get())

# 第5步，在視窗介面設定放置Button按鍵
#b = tk.Button(window, text='connect', font=('Arial', 12), width=10, height=1, command=connect)
#b.pack()
takeoff = tk.Button(window, text='takeoff', font=('Arial', 12), width=30, height=1, command=arm_and_takeoff, fg='green')
takeoff.pack()
RTL = tk.Button(window, text='RTL', font=('Arial',12),width=20, height=1, command=rtl, fg='red')
RTL.pack()
mode = tk.Button(window, text='設定', font=('Helvetica', 12), width=20, height=1, command=mode)
mode.pack()

#執行mode_select()
mode_select()
# 第6步，主視窗迴圈顯示
window.mainloop()
vehicle.close()