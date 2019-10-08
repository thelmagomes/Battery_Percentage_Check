from ctypes import *
import os
import tkinter as tk
import sys
import datetime as dt
import subprocess

FONT=("Verdana", 12)
DATETIME='\n'+ str(dt.datetime.today().strftime('%d-%m-%Y  %H:%M:%S'))

class BatteryClass(Structure):
    _fields_=[('ACLineStatus', c_byte),
              ('BatteryFlag', c_byte),
              ('BatteryLifePercent', c_byte)]

def displayBattery(message):
    display=tk.Tk()
    display.wm_title("Battery Alert")

    w=300 
    h=150 
    ws=display.winfo_screenwidth()
    wh=display.winfo_screenheight()
    x=(ws/2)-(w/2)
    y=(wh/2)-(h/2)
    display.geometry('+%d+%d' %(x,y))
    display.configure(bg="aqua")
    label=tk.Label(display, text=message, font=FONT, bg='aqua', fg='red')
    label.pack(side="top", fill='both', pady=10, padx=10)
    button=tk.Button(display, text='Thanks for informing!',fg='red', bg='white', command=display.destroy)
    button.pack(side='bottom', pady=10)
    display.mainloop()
    
if __name__== '__main__':
    batteryclass=BatteryClass()
    r=windll.kernel32.GetSystemPowerStatus(byref(batteryclass))

    ac="The Laptop is currently charging." if batteryclass.ACLineStatus == 1 else "The Laptop NEEDS charging."
    batt=batteryclass.BatteryLifePercent
    print (batteryclass.BatteryLifePercent)

    if batt <= 45:
        displayBattery("The battery is now at "+ str(batt) + ".\n" + ac + DATETIME)
    elif batt ==100 and batteryclass.ACLineStatus == 1 :
        displayBattery("The battery is now at "+ str(batt) + "!\nYou may now unplug the charger." + DATETIME)

    cmdWindow = windll.kernel32.GetConsoleWindow()      
    if cmdWindow != 0:      
        windll.user32.ShowWindow(cmdWindow, 0)      
        windll.kernel32.CloseHandle(cmdWindow)
        pid = os.getpid(cmdWindow)
        #os.system('taskkill /PID ' + str(pid) + ' /f')
        subprocess.Popen('taskkill /PID ' + str(pid) + ' /f', shell=True)
        #si = subprocess.STARTUPINFO()
        #si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #si.wShowWindow = subprocess.SW_HIDE # default
        #subprocess.call('taskkill /PID ' + str(pid) + ' /f', startupinfo=si)

