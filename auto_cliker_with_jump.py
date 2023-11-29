import tkinter as tk
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener, KeyCode
import threading
import time
import keyboard
import pygetwindow as gw

class AutoClicker:
    def __init__(self, interval=0.20, hotkey_start="9", hotkey_stop="0"):
        self.interval = interval
        self.running = False
        self.hotkey_start = KeyCode.from_char(hotkey_start)
        self.hotkey_stop = KeyCode.from_char(hotkey_stop)
        self.mouse = MouseController()
        self.auto_clicker_thread = None
        self.jump_disabled = False  # Флаг для отключения прыжка

    def start_clicking(self):
        self.running = True
        while self.running:
            self.mouse.click(Button.left)
            if not self.jump_disabled:  # Добавлено условие для прыжка
                keyboard.press_and_release('space')
            time.sleep(self.interval)

    def stop_clicking(self):
        self.running = False

def disable_jump():
    auto_clicker.jump_disabled = True

def enable_jump():
    auto_clicker.jump_disabled = False

def start_auto_clicker():
    auto_clicker.auto_clicker_thread = threading.Thread(target=auto_clicker.start_clicking)
    auto_clicker.auto_clicker_thread.start()
    status_var.set("Running")

    # Отключаем прыжок на 5 секунд
    disable_jump_timer = threading.Timer(5, disable_jump)
    disable_jump_timer.start()

    # Включаем прыжок после 5 секунд
    enable_jump_timer = threading.Timer(10, enable_jump)
    enable_jump_timer.start()

def stop_auto_clicker():
    auto_clicker.stop_clicking()
    if auto_clicker.auto_clicker_thread is not None:
        auto_clicker.auto_clicker_thread.join()
    status_var.set("Stopped")

def press_space_periodically():
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            keyboard.press_and_release('space')
    except Exception as e:
        print(f"Error: {e}")

    root.after(10, press_space_periodically)

def on_key_release(key):
    if key == auto_clicker.hotkey_start:
        start_auto_clicker()
    elif key == auto_clicker.hotkey_stop:
        stop_auto_clicker()

root = tk.Tk()
root.title("AutoClicker")

auto_clicker = AutoClicker()

start_button = tk.Button(root, text=f"Start AutoClicker (Hotkey: {auto_clicker.hotkey_start})", command=start_auto_clicker)
start_button.pack()

stop_button = tk.Button(root, text=f"Stop AutoClicker (Hotkey: {auto_clicker.hotkey_stop})", command=stop_auto_clicker)
stop_button.pack()

with KeyboardListener(on_release=on_key_release):
    status_var = tk.StringVar()
    status_var.set("Stopped")
    status_label = tk.Label(root, textvariable=status_var)
    status_label.pack()

    root.after(60, press_space_periodically)

    root.mainloop()
