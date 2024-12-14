import hashlib
import telnetlib
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
from random import randrange
from sage.all import *

curve_gen = generator_192
curve_order = curve_gen.order()

SERVER_HOST = "socket.cryptohack.org"
SERVER_PORT = 13381

def recv_line(tn_connection):
    return tn_connection.read_until(b"\n")

def send_json(tn_connection, payload):
    tn_connection.write(json.dumps(payload).encode())

def receive_json(tn_connection):
    l = recv_line(tn_connection).decode()
    start_idx = l.find('{')
    return json.loads(l[start_idx:])

def compute_sha1(data):
    sha1_instance = hashlib.sha1()
    sha1_instance.update(data)
    return sha1_instance.digest()

def sign_message(message, private_key, k_value):
    message_hash = compute_sha1(message.encode())
    signature = private_key.sign(bytes_to_long(message_hash), k_value)
    return hex(signature.r), hex(signature.s)

print("Connecting to server...")
tn = telnetlib.Telnet(SERVER_HOST, SERVER_PORT)
print(recv_line(tn))

request_payload = {"option": "sign_time"}
send_json(tn, request_payload)
server_response = receive_json(tn)
print("Server Response:", server_response)

received_message = server_response["msg"]
received_r = int(server_response["r"], 16)
received_s = int(server_response["s"], 16)

max_attempts = 60
fm = "unlock"

for trial_k in range(1, max_attempts + 1):
    try:
        R_mod_n = Integers(curve_order)
        message_hash_value = bytes_to_long(compute_sha1(received_message.encode()))
        
        recovered_secret = int(
            R_mod_n((received_s * trial_k) - message_hash_value) // R_mod_n(received_r)
        )

        public_key = Public_key(curve_gen, curve_gen * recovered_secret)
        private_key = Private_key(public_key, recovered_secret)

        r_signature, s_signature = sign_message(fm, private_key, trial_k)

        verification_payload = {
            "option": "verify",
            "msg": fm,
            "r": r_signature,
            "s": s_signature
        }
        send_json(tn, verification_payload)
        
        response = recv_line(tn)
        print("Trial {}: {}".format(trial_k, response.decode()))
    
    except Exception as e:
        continue

# it requests a signature from server and attempts to recover the private key using elliptic curve signature and brute force.
# with no. of iterations, it tries to find a valid key to generate a valid signature.
# process continues until a valid signature is found.