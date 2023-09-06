import time
import os
import threading as thread
import pathlib
import sys
from tkinter import Tk, Frame, Label, RAISED
from PIL import Image, ImageTk

PATH = str(pathlib.Path(__file__).parent.absolute())
os.chdir(PATH)
scalar = 0.6

SYS_ARGS = sys.argv.copy()
SYS_ARGS.pop(0)

def doAnimation():
    root = Tk()
    root.configure(bg='black')
    root.frame = Frame(root, borderwidth=2, relief=RAISED)
    root.wm_attributes('-topmost', 1)
    root.overrideredirect(1)

    if len(SYS_ARGS) >= 1 and SYS_ARGS[0] == '-custom':
        img_ = Image.open(os.path.join(PATH, 'resource', 'loading_splash.png'))
    else:
        img_ = Image.open(os.path.join(PATH, 'default_assets', 'loading_splash.png'))
    if len(SYS_ARGS) >= 2 and SYS_ARGS[1] == '-lanczos' or len(SYS_ARGS) == 1 and SYS_ARGS[0] == '-lanczos':
        img = ImageTk.PhotoImage(img_.resize((int(img_.width * scalar), int(img_.height * scalar)), resample=Image.LANCZOS))
    else:
        img = ImageTk.PhotoImage(img_.resize((int(img_.width * scalar), int(img_.height * scalar)), resample=Image.ANTIALIAS))
    root.geometry('{}x{}+{}+{}'.format(img.width(), img.height(), int((root.winfo_screenwidth() - img.width()) / 2), int((root.winfo_screenheight() - img.height()) / 2)))
    lbl = Label(root, image=img)
    lbl.pack()
    root.attributes('-alpha', 0)
    thread.Thread(target=lambda: anim(root)).start()
    root.mainloop()

def anim(root):
    alpha = 0.0
    step = 0.01
    for i in range(int(1 / step)):
        root.attributes('-alpha', alpha)
        alpha += step
        time.sleep(step)
    time.sleep(2)
    for i in range(int(1 / (2*step))):
        root.attributes('-alpha', alpha)
        alpha -= 2*step
        time.sleep(step/4)

    os.kill(os.getpid(), 9)

doAnimation()
