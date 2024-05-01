import subprocess
import sys

from EdgeWare.utils.paths import Process

print("""Which feature would you like to run?
0. Quit
1. Edgeware (start.pyw)
2. Config (config.pyw)
3. Image popup (popup.pyw)
4. Video popup (popup.pyw)
5. Prompt (prompt.pyw)
6. Subliminal message (sublabel.pyw)""")

processes = [
    [Process.START],
    [Process.CONFIG],
    [Process.POPUP],
    [Process.POPUP, "-video"],
    [Process.PROMPT],
    [Process.SUBLABEL]
]

while True:
    num = input("Select number: ")
    try:
        num = int(num)
    except Exception:
        print("Input must be an integer")
        continue

    if num == 0:
        break
    elif num > 0 and num <= len(processes):
        subprocess.run([sys.executable] + processes[num - 1])
        print("Done")
    else:
        print("Input must be between 0 and 6")

print("Goodbye!")
