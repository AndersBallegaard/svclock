# SVCLock
### Make sure only one instance is active, without any of the instances needing to know where or how many other instances are alive

## Interact with SVCLock
### /lock
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