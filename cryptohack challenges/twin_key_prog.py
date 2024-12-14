from Crypto.Util.number import bytes_to_long, long_to_bytes
import telnetlib
import json
import re
from pkcs1 import emsa_pkcs1_v15
from sage.all import *
import fastecdsa
from fastecdsa.point import Point

HOST = "socket.cryptohack.org"
PORT = 13397

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline().decode()
    st = line[line.find('{'):]
    return json.loads(st)

def json_send(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)

p1 = "43727970746f4861636b205365637572652053616665300a08de6e639eb76baa3f782925580a654ad735580c928d0e6936fecd35ebd5ac2d6bc4608b6e55239ddee23a8ae2c6bdcdf57745c78aef60b46903e9b3eb4e128ad05ab9f459839ccd8374ca53aa802edd2cba35bf081d2b7ae96e70787c391cf11bcc226565219236"
p2 = "43727970746f4861636c205365637572652053616665300a08de6e639eb76baa3f782925580a654ad735580c928d0e6936fecd35ebd5ac2d6bc4608b6e55239ddee23a8ae2c6bdcdf57645c78aef60b46903e9b3eb4e128ad05ab9f459839ccd8374ca53aa802edd2cba35bf081d2b7ae96e70787c391cf11bcc226565219236"

tn = telnetlib.Telnet(HOST, PORT)
print(readline())

to_send = json.loads(json.dumps({"option" : "insert_key", "key" : p1}))
json_send(to_send)
print(json_recv())
to_send = json.loads(json.dumps({"option" : "insert_key", "key" : p2}))
json_send(to_send)
print(json_recv())
to_send = json.loads(json.dumps({"option" : "unlock"}))
json_send(to_send)
print(json_recv())

# it connects to telnet server and inserts two keys p1 and p2 into server.
# for each iteration, the response is printed.
# Finally, it sends request to unlock something using the keys and prints response.