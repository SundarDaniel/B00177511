from Crypto.Util.number import bytes_to_long, long_to_bytes
import telnetlib
import json
import re
from pkcs1 import emsa_pkcs1_v15
from sage.all import *

HOST = "socket.cryptohack.org"
PORT = 13376

def r_line():
    return tn.read_until(b"\n")

def r_json():
    line = r_line().decode()
    st = line[line.find('{'):]
    return json.loads(st)

def s_json(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)

tn = telnetlib.Telnet(HOST, PORT)

ADMIN_TOKEN = b"admin=True"

print(r_line())
to_send = json.loads(json.dumps({"option" : "get_pubkey"}))
s_json(to_send)

p = r_json()
n = int(p["N"][2:],16)
e = int(p["e"][2:],16)

msg = hex(bytes_to_long(ADMIN_TOKEN) + n)
to_send = json.loads(json.dumps({"option" : "sign", "msg" : msg[2:]}))
s_json(to_send)
p = r_json()

sig = int(p["signature"][2:],16)

to_send = json.loads(json.dumps({"option" : "verify", "signature" : hex(sig), "msg" : ADMIN_TOKEN.hex()}))
s_json(to_send)
p = r_json()
print(p)

# it connects to a remote server and obtains rsa public key. then it creates a message and
# signs the message using server's functionality.
# finally, verifys the signature using the server's verify option.