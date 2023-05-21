import pyautogui
import time

filename = "powershell.txt" # replace with the name of your file
with open(filename, "r") as f:
    text = f.read()

time.sleep(3)
for char in text:
    pyautogui.typewrite(char)
    time.sleep(10/1000)
    if char == '\n':
        time.sleep(0.5) # add a bit longer delay for Enter keystrokes
