#!/usr/bin/python3
import os
from flask import Flask, request, jsonify
import json
import datetime

# Create app object
app = Flask(__name__)

# Check if config.json is valid and load it
config = {}
if not os.path.exists('config.json'):
    raise FileNotFoundError('config.json not found')

with open("config.json") as f:
    config = json.loads(f.read())
    
if "locks" not in config.keys():
    raise KeyError("locks list not found in config")

if type(config["locks"]) is not list:
    raise TypeError("locks not list")

if len(config["locks"]) is 0:
    raise ValueError("Locks list is empty")

for lock in config["locks"]:
    if type(lock) is not dict:
        raise TypeError("Lock not type dict")
    if "name" not in lock.keys():
        raise KeyError("Lock missing name")
    if "hello_time" not in lock.keys():
        raise KeyError(f"Lock {lock['name']} missing hello timer")
    if "dead_time" not in lock.keys():
        raise KeyError(f"Lock {lock['name']} missing dead timer")
    if lock["hello_time"] >= lock["dead_time"]:
        raise ValueError(f"Lock {lock['name']} hello timer greater or equal to dead time")

lock_manager = {}

for lock in config["locks"]:
    lock_manager[lock["name"]] = (None,None)


@app.route("/lock", methods=["GET"])
def lock_api():
    active = False
    hello_time = 0
    dead_time = 0
    
    lock_name = str(request.args.get('name'))
    instance_id = str(request.args.get('instance'))
    
    for name, status in lock_manager.items():
        #print(name.encode('utf-8').hex())
        #print(lock_name.encode('utf-8').hex())
        # Overcomplicated but for some reason this seems to work better
        if name.encode('utf-8').hex() == lock_name.encode('utf-8').hex():

            l = None
            for l0 in config["locks"]:
                if l0["name"] == name:
                    l = l0
            
            if status[1] == None\
                or status[0] == instance_id\
                or datetime.datetime.now()  > status[1] + datetime.timedelta(seconds=l["dead_time"]):

                
                active = True
    if active:
        lock_manager[lock_name] = (instance_id, datetime.datetime.now())
    for l0 in config["locks"]:
        
        if l0["name"] == lock_name:
            
            hello_time = l0["hello_time"]
            dead_time = l0["dead_time"]
    

    r = {
        "active" : active,
        "hello" : hello_time,
        "dead" : dead_time
    }
    return jsonify(r)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)