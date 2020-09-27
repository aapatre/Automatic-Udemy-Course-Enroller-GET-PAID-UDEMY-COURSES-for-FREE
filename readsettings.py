import json

f = open("./settings.json",)
settings = json.load(f)

for setting in settings ['settings']:
    print(setting['username'])
    print(setting['password'])
    print(setting['driver_path'])
    
f.close()