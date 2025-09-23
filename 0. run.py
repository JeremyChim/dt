import subprocess
import shutil
import time

subprocess.run(r"C:\Users\Jeremy\Desktop\dt\vpk\vpk.bat", shell=True)
time.sleep(0.1)
shutil.move(r"C:\Users\Jeremy\Desktop\dt\vpk\pak01_dir.vpk", r"C:\Users\Jeremy\Desktop\dt\pak01_dir.vpk")