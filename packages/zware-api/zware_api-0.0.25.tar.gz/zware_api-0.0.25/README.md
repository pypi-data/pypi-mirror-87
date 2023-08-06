# ZWare API

The zwave controller was developed for z-wave 700 series. Is a client that works with Z/IP Gateway SDK and Z-Ware SDK.


### Example

```zw = ZWareApi()

zwC = zwClient(zw, 'host', 'user', 'pass')
zwC.login()

print (zwC.get_node_list())
```
