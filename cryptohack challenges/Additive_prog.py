from Crypto.Util.number import bytes_to_long, long_to_bytes
import base64
import codecs
import random
import telnetlib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from sage.all import *

def check_pkcs7_padding(data):
    padding = data[-data[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_message(shared_key: int, iv_str: str, encrypted_data: str):
    # Derive AES key from shared key
    sha1 = hashlib.sha1()
    sha1.update(str(shared_key).encode('ascii'))
    aes_key = sha1.digest()[:16]
    # Decrypt message
    encrypted_data = bytes.fromhex(encrypted_data)
    iv = bytes.fromhex(iv_str)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)

    if check_pkcs7_padding(decrypted_data):
        return unpad(decrypted_data, 16).decode('ascii')
    else:
        return decrypted_data.decode('ascii')


SERVER_HOST = "socket.cryptohack.org"
SERVER_PORT = 13380

def read_line():
    return tn.read_until(b"\n")

def receive_json():
    line = read_line().decode()
    start_idx = line.find('{')
    return json.loads(line[start_idx:])

def send_json(data):
    request = json.dumps(data).encode()
    tn.write(request)
    
tn = telnetlib.Telnet(SERVER_HOST, SERVER_PORT)

alice_data = receive_json()
bob_data = receive_json()
flag_data = receive_json()

R = GF(alice_data["p"])
g = R(alice_data["g"])
A = R(alice_data["A"])
B = R(bob_data["B"])

a_value = A/g
b_value = B/g

shared_key = b_value*A
print(decrypt_message(shared_key, flag_data['iv'], flag_data['encrypted']))

# it connects to a server to get public keys for Alice and Bob and a flag.
# It computes shared secret between Alice and Bob using Diffie hellman key exchange and gets a key 
# and decrypts a flag using the new key.