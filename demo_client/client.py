#!/usr/bin/python3
import time
import threading
import requests
import uuid

iid = uuid.uuid1()


def get_lock(lock_name, host="127.0.0.1"):
    r = {"active": False, "hello": 0, "dead": 0}

    try:
        lock_resp = requests.get(
            f"http://{host}:5050/lock?name={lock_name}&instance={iid}"
        )
        r1 = lock_resp.json()
        # print(r1)
        if "active" in r1.keys() or "hello" in r1.keys() or "dead" in r1.keys():
            r = r1
    except Exception as e:
        print("Encountered error: " + e)

    return r


is_active = False
lock = {"active": False, "hello": 1, "dead": 0}


def lock_thread(lock_name="default"):
    global lock
    global is_active
    while True:
        # print("Running")
        l = get_lock(lock_name)
        lock = l
        is_active = l["active"]
        time.sleep(l["hello"])


if __name__ == "__main__":
    t = threading.Thread(target=lock_thread)
    t.start()

    while True:
        time.sleep(10)
        print(f"Status: {is_active}")
        print(lock)
