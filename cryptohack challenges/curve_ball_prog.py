from Crypto.Util.number import bytes_to_long, long_to_bytes
import telnetlib
import json
from fastecdsa.point import Point
from fastecdsa.curve import P256
from sage.all import *
import re

SERVER_HOST = "socket.cryptohack.org"
SERVER_PORT = 13382

def establish_connection():
    return telnetlib.Telnet(SERVER_HOST, SERVER_PORT)

def recv_line(tn):
    """Receive a single line from the server."""
    return tn.read_until(b"\n")

def send_json(tn, data):
    """Send a JSON-encoded message to the server."""
    request = json.dumps(data).encode()
    tn.write(request)

def recv_json(tn):
    """Receive and parse a JSON message."""
    line = recv_line(tn).decode()
    json_start = line.find('{')
    return json.loads(line[json_start:])

def generate_new_generator():
    """Generate a new generator based on secp256r1 and a given point."""
    base_point = P256.G  
    custom_x = 0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531
    custom_y = 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A
    custom_point = Point(custom_x, custom_y)
    
    q_mod = Integers(P256.q)
    new_generator = int(1 // q_mod(3)) * custom_point
    return new_generator

if __name__ == "__main__":
    print("Connecting to server...")
    telnet = establish_connection()
    print(recv_line(telnet)) 

    generator_point = generate_new_generator()
    payload = {
        "private_key": 3,
        "host": "www.bing.com",
        "curve": "secp256r1",
        "generator": [generator_point.x, generator_point.y]
    }

    print("Sending modified generator...")
    send_json(telnet, payload)
    response = recv_line(telnet)
    print("Server Response:", response.decode())

# it establishes a telenet connection with a server and interacts with it.
# it generates a custom elliptic curve, modifies it with scalar multiplication and sends it to server.
# the server response is the result 