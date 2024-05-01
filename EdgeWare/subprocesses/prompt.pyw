import json
import os
import random as rand
import sys
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import font, messagebox

from screeninfo import get_monitors

sys.path.append(str(Path(__file__).parent.parent))
from utils import utils
from utils.paths import Data, Resource

SYS_ARGS = sys.argv.copy()
SYS_ARGS.pop(0)


hasData = False
textData = {}
maxMistakes = 3
submission_text = "I Submit <3"
command_text    = "Type for me, slut~"
moodData = {}
THEME = "Original"


with open(Data.CONFIG) as settings:
    jsondata = json.loads(settings.read())
    maxMistakes = int(jsondata["promptMistakes"])
    THEME = jsondata["themeType"]

MOOD_ID = "0"
if len(SYS_ARGS) >= 1 and SYS_ARGS[0] != "0":
    MOOD_ID = SYS_ARGS[0].strip("-")

if MOOD_ID != "0":
    if os.path.exists(Data.MOODS / f"{MOOD_ID}.json"):
        with open(Data.MOODS / f"{MOOD_ID}.json", "r") as f:
            moodData = json.loads(f.read())
    elif os.path.exists(Data.UNNAMED_MOODS / f"{MOOD_ID}.json"):
        with open(Data.UNNAMED_MOODS / f"{MOOD_ID}.json", "r") as f:
            moodData = json.loads(f.read())

if os.path.exists(Resource.PROMPT):
    hasData = True
    with open(Resource.PROMPT, "r") as f:
        textData = json.loads(f.read())
        try:
            submission_text = textData["subtext"]
        except:
            print("no subtext")
        try:
            command_text = textData["commandtext"]
        except:
            print("no commandtext")

if not hasData:
    messagebox.showerror("Prompt Error", 'Resource folder contains no "prompt.json". Either set prompt freq to 0 or add "prompt.json" to resource folder.')

def unborderedWindow():
    if not hasData:
        exit()
    root = Tk()

    fore = "#000000"
    back = "#f0f0f0"
    textb = "#ffffff"
    textf = "#000000"
    mainfont = font.nametofont("TkDefaultFont")

    if THEME == "Dark":
        fore = "#f9faff"
        back = "#282c34"
        textb = "#1b1d23"
        textf = "#f9faff"
    if THEME == "The One":
        fore = "#00ff41"
        back = "#282c34"
        textb = "#1b1d23"
        textf = "#00ff41"
        mainfont.configure(family="Consolas", size=8)
    if THEME == "Ransom":
        fore = "#ffffff"
        back = "#841212"
        textb = "#ffffff"
        textf = "#000000"
        mainfont.configure(family="Arial Bold")
    if THEME == "Goth":
        fore = "#ba9aff"
        back = "#282c34"
        textb = "#db7cf2"
        textf = "#6a309d"
        mainfont.configure(family="Constantia")
    if THEME == "Bimbo":
        fore = "#ff3aa3"
        back = "#ffc5cd"
        textb = "#ffc5cd"
        textf = "#f43df2"
        mainfont.configure(family="Constantia")

    root.configure(background=back)
    label = tk.Label(root, text="\n" + command_text + "\n", bg=back, fg=fore)
    label.pack()

    txt = buildText()

    monitor = rand.choice(get_monitors()) # TODO: Only on primary monitor?
    wid = monitor.width / 4
    hgt = monitor.height / 2

    textLabel = Label(root, text=txt, wraplength=wid, bg=back, fg=fore)
    textLabel.pack()

    root.geometry("%dx%d+%d+%d" % (wid, hgt, monitor.x + 2*wid - wid / 2, monitor.y + hgt - hgt / 2))

    root.frame = Frame(root, borderwidth=2, relief=RAISED, bg=back)
    root.frame.pack_propagate(True)
    root.wm_attributes("-topmost", 1)
    utils.set_borderless(root)

    inputBox = Text(root, bg=textb, fg=textf)
    inputBox.pack()

    subButton = Button(root, text=submission_text, command=lambda: checkTotal(root, txt, inputBox.get(1.0, "end-1c")), bg=back, fg=fore,
                       activebackground=back, activeforeground=fore)
    subButton.place(x=wid - 5 - subButton.winfo_reqwidth(), y=hgt - 5 - subButton.winfo_reqheight())
    root.mainloop()

def buildText():
    moodList = textData["moods"]
    freqList = textData["freqList"]
    if MOOD_ID != "0":
        for i, mood in enumerate(moodList):
            if mood not in moodData["prompts"]:
                del moodList[i-1]
                del freqList[i-1]
    outputPhraseCount = rand.randint(int(textData["minLen"]), int(textData["maxLen"]))
    strVar = ""
    selection = rand.choices(moodList, freqList, k=1)
    for i in range(outputPhraseCount):
        strVar += textData[selection[0]][rand.randrange(0, len(textData[selection[0]]))] + " "
    #strVar += MOOD_ID
    return strVar.strip()

# Checks that the number of mistakes is at most maxMistakes and if so,
# closes the prompt window. The number of mistakes is computed as the edit
# (Levenshtein) distance between a and b.
# https://en.wikipedia.org/wiki/Levenshtein_distance
def checkTotal(root, a, b):
    d = [[j for j in range(0, len(b) + 1)]] + [[i] for i in range(1, len(a) + 1)]

    for j in range(1, len(b) + 1):
        for i in range(1, len(a) + 1):
            d[i].append(min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1)
            ))

    if d[len(a)][len(b)] <= maxMistakes:
        root.destroy()

try:
    unborderedWindow()
except Exception as e:
    messagebox.showerror("Prompt Error", "Could not create prompt window.\n[" + str(e) + "]")
