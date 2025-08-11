import json
import os

file = "rulesAccepted.json"

if not os.path.exists(file):
    with open(file, "w") as f:
        json.dump({"accepted": []}, f)

def loadAccepted():
    with open(file, "r") as f:
        return json.load(f)["accepted"]

def saveAccepted(data):
    with open(file, "w") as f:
        json.dump({"accepted": data}, f, indent=4)

def hasAccepted(user_id):
    return user_id in loadAccepted()

def setAccepted(user_id):
    data = loadAccepted()
    if user_id not in data:
        data.append(user_id)
        saveAccepted(data)

def removeAccepted(user_id):
    data = loadAccepted()
    if user_id in data:
        data.remove(user_id)
        saveAccepted(data)
