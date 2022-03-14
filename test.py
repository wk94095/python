import serial.tools.list_ports
import tkinter as tk
import time
from dronekit import connect

vehicle = connect('COM8', wait_ready=True,baud=115200)

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

var.set(vehicle.mode.name)
       
window.mainloop()
vehicle.close()