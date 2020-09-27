import json

f = open("./settings.json",)
settings = json.load(f)

for i in settings ['settings']:
    print(i['username'])
    print(i['password'])
    print(i['driver_path'])
    
f.close()