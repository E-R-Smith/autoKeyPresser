
import tkinter as tk
import tkinter.scrolledtext as st
from time import sleep
from functools import partial
from threading import Thread
import datetime
from pynput.keyboard import Key, Controller
import ctypes

myappid = u'ersolstice.keypreser.v0.1' #https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# adapted from https://stackoverflow.com/questions/67999559/start-and-stop-a-repeating-task-in-a-thread-from-a-button-in-tkinter

# GLOBALS #
running_job = False
kb = Controller()
log = ""
logArea = None
# ----- #


def presskey():
    global log
    global logArea

    kb.press('F')
    kb.release('F')
    now = datetime.datetime.now()
    log.set(log.get() + now.strftime("%H:%M:%S") + ": Paid Respects\n")
    logArea.insert('1.0', now.strftime("%H:%M:%S") + ": Paid Respects\n")
    sleep(0.5)

def kickoff():
    global log
    global logArea
    
    log.set(log.get() + "Starting in\n")
    logArea.insert('1.0', "Starting in\n")
    for i in range(3, 0, -1):
        if not running_job:
            break # for when STOP is pressed before countdown ends
        log.set(f"{i}...\n")
        logArea.insert('1.0', f"{i}...\n")
        sleep(1)

    while running_job:
        presskey()
    log.set(log.get() + "Stopped\n")
    logArea.insert('1.0', "Stopped\n")


class GUI:
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master)

        command = partial(run_threaded, kickoff)
        self.button1 = tk.Button(text="Start", command=command)
        self.button1.pack()
        self.button2 = tk.Button(text="Stop", command=stop_button)
        self.button2.pack()


def run_threaded(job_func):
    global running_job
    running_job = True
    job_thread = Thread(target=job_func, daemon=True)
    job_thread.start()

def stop_button():
    global running_job
    running_job = False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Respectful")
    root.geometry("250x150")
    root.iconbitmap('./assets/icon.ico')
    root.configure(background='#8bb500')
    log = tk.StringVar()
    log.set("")
    app = GUI(root)
    
    logArea = st.ScrolledText(root, width = 25, height = 5)
    logArea.pack()

    #lbl = tk.Label(root, textvariable=log)
    #lbl.pack()
    root.mainloop()