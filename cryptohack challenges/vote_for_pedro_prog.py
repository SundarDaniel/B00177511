from Crypto.Util.number import bytes_to_long, long_to_bytes
import telnetlib
import json
import re
from pkcs1 import emsa_pkcs1_v15
from sage.all import *

HOST = "socket.cryptohack.org"
PORT = 13375

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
r_line()

N = 22266616657574989868109324252160663470925207690694094953312891282341426880506924648525181014287214350136557941201445475540830225059514652125310445352175047408966028497316806142156338927162621004774769949534239479839334209147097793526879762417526445739552772039876568156469224491682030314994880247983332964121759307658270083947005466578077153185206199759569902810832114058818478518470715726064960617482910172035743003538122402440142861494899725720505181663738931151677884218457824676140190841393217857683627886497104915390385283364971133316672332846071665082777884028170668140862010444247560019193505999704028222347577
e = 3
M = 2**120

a = bytes_to_long(b'VOTE FOR PEDRO')
W = Integers(M//2)
d1 = int(1//W(3))

W = Integers(M)
b = int(W(a)**d1)

i = ((b**3)-a)//M

to_send = json.loads(json.dumps({"option" : "vote", "vote" : hex(b)[2:]}))
json_send(to_send)
p = json_recv()
print(p)

# The code connects to a remote server and sends a vote in a encrypted format. 
# It uses modular arithmetic to manipulate and compute values.
# Finally, it constructs and sends request and prints the result.