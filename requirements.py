import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("selenium")
install("requests")
install("beautifulsoup4")
install("webdriver-manager")

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'selenium'])
print(reqs)
print("\n If you can read the above message, SELENIUM has been successfully installed! \n")

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'requests'])
print(reqs)
print("\n If you can read the above message, REQUESTS has been successfully installed! \n")

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'beautifulsoup4'])
print(reqs)
print("\n If you can read the above message, BEAUTIFUL SOUP 4 has been successfully installed! \n")

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'webdriver-manager'])
print(reqs)
print("\n If you can read the above message, WEBDRIVER-MANAGER has been successfully installed! \n")
