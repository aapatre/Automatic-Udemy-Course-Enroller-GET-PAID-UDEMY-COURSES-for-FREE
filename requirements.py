import subprocess
import sys
import os

def install(package):
    #subprocess.check_call([sys.executable, "-m", "pip", "install", str(package)])
    os.system("pip install "+ str(package))
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'show', str(package)])

    print(str(reqs) + "\n")
    print("Installed " + package.upper() + "\n")

install("requests")
install("beautifulsoup4")
install("ruamel.yaml")
install("selenium")
install("webdriver_manager")