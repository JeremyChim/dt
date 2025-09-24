import subprocess
import shutil
import time
import pyperclip

# 运行vpk.bat
subprocess.run(r"C:\Users\Jeremy\Desktop\dt\vpk\vpk.bat", shell=True)
time.sleep(0.1)
# 移动pak01_dir.vpk
shutil.move(r"C:\Users\Jeremy\Desktop\dt\vpk\pak01_dir.vpk", r"C:\Users\Jeremy\Desktop\dt\pak01_dir.vpk")
# bot指令
pyperclip.copy("sv_cheats 1; script_reload_code bots/fretbots")

time.sleep(3)