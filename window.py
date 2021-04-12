import tkinter as tk
from tkinter import ttk
from EDSM import refresh
import threading
import time

count = 0


def show(amount):
    bar.config(value=amount)
    label.config(text="Progress: " + str(amount) + "%")


def window(height=100, width=300):
    global bar, label
    root = tk.Tk()
    root.title("EDLaunchpad")
    root.resizable(False, False)
    ttk.Style().theme_use('vista')

    def auto_refresh(secs=60):
        time.sleep(1)
        while count == 1:
            refresh()
            time.sleep(secs)

    def cb_command():
        global count
        if count == 0:
            threading.Thread(target=auto_refresh).start()
            count = 1
        else:
            count = 0

    canvas = tk.Canvas(root, height=height, width=width)
    canvas.pack()

    frame = tk.Frame(root, bd=10)
    frame.place(relheight=1, relwidth=1)

    label = ttk.Label(frame, text="Progress: ")
    label.grid(row=0, column=0, padx=5, pady=3, sticky="W")

    refresh_button = ttk.Button(frame, text="Refresh", command=refresh)
    refresh_button.grid(row=0, column=1, padx=5, ipadx=20, sticky="E")

    checkbox = ttk.Checkbutton(frame, text="Auto Refresh", command=cb_command)
    checkbox.grid(row=2, column=0, padx=5, pady=3, sticky="W")

    bar = ttk.Progressbar(frame, mode="determinate", value=0, length=270)
    bar.grid(row=1, column=0, columnspan=2, padx=5, pady=3, sticky="W")

    root.mainloop()

if __name__ == "__main__":
    import main