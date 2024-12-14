from Crypto.Util.number import bytes_to_long, long_to_bytes
import telnetlib
import json
import re
from pkcs1 import emsa_pkcs1_v15
from sage.all import *
import fastecdsa
from fastecdsa.point import Point

HOST = "socket.cryptohack.org"
PORT = 13389


def r_line():
    return tn.read_until(b"\n")

def json_recv():
    line = r_line().decode()
    st = line[line.find('{'):]
    return json.loads(st)

def json_send(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)

tn = telnetlib.Telnet(HOST, PORT)
print(r_line())

to_send = json.loads(json.dumps({"document" : "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"}))
json_send(to_send)
print(r_line())

to_send = json.loads(json.dumps({"document" : "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"}))
json_send(to_send)
print(r_line())

# it connects to a server and prints the server responses. 
# json documents contains long hexadecimal strings related to cryptographic operations.
# json_send() to send and json_recv() to get the responses.