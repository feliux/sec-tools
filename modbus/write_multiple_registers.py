import socket
from umodbus import conf
from umodbus.client import tcp

_MODBUS_HOST = "10.0.2.12"
_SLAVE_ID = 1
_DATA_ADDRESS = 0
_LIST_VALUES = [1, 1, 1, 1]

conf.SIGNED_VALUES = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((_MODBUS_HOST, 502))

message = tcp.write_multiple_registers(slave_id=_SLAVE_ID, starting_address=_DATA_ADDRESS, values=_LIST_VALUES)
response = tcp.send_message(message, sock)
print(response)

sock.close()
