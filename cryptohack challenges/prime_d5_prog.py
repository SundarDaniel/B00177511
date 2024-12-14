from Crypto.Util.number import bytes_to_long, long_to_bytes
import telnetlib
import json
import re
from pkcs1 import emsa_pkcs1_v15
from sage.all import *
import fastecdsa
from fastecdsa.point import Point

HOST = "socket.cryptohack.org"
PORT = 13392

def r_line():
    return tn.read_until(b"\n")

def json_recv():
    line = r_line().decode()
    st = line[line.find('{'):]
    return json.loads(st)

def json_send(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)

p1 = 168372483594051730655820996690138951969774005433766395387688615584540140900710691132801423560880645636787567562700867844996261531963192453964591654200576712262132526428152200379167640852910063046101763828915652400127047206140061076598343986693012019419450608867077881990659651358706028092457741758989240675419
p2 = 168372483594051730655820847988448104191467725627516580397632602458519974961264785555615491966814929596350213045869418229361202552090813434667286608742052157771561747345094090139716153234602501559552683217011241305167105930521986107755305298240599816862664295649343744749267908466585047521912073669770255838299

tn = telnetlib.Telnet(HOST, PORT)
print(r_line())

to_send = json.loads(json.dumps({"option" : "sign", "prime" : p1}))
json_send(to_send)
sig = json_recv()
to_send = json.loads(json.dumps({"option" : "check", "prime" : p2, "signature" : sig["signature"], "a" : 3119}))
json_send(to_send)
print(json_recv())

# code connects to a telnet server and sends a request to sign a prime no. 
# then it send the resulting signature to check against another prime number. Response is printed.