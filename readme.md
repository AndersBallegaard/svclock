# SVCLock
### Make sure only one instance is active, without any of the instances needing to know where or how many other instances are alive

## Interact with SVCLock
### http://{server}:5050/lock
```http
Type: Get
Arguments:
    - name = str # Name of lock
    - instance = str # A uniqe string for a host. A simple choice would be hostname

Response
{
    "active" : True/False,
    "hello" : int, # The recomended hello interval in secounds
    "dead" : int # The dead interval for the lock
}
```

## Test it!
1. start server
```bash
cd server
python3 svclock_server.py
```
2. start a client
```bash
cd demo_client
python3 client.py
```
3. Start more clients
```
Repeat step 2
```

