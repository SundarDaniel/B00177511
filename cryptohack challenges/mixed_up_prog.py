from Crypto.Util.number import bytes_to_long, long_to_bytes
import telnetlib
import json
from sage.all import *
from hashlib import sha256
import os

def validate_hash(value, length):
    for char in range(256):
        if value == sha256(bytes([char] * length)).hexdigest():
            return True
    return False

server_host = "socket.cryptohack.org"
server_port = 13402

def read_line():
    return connection.read_until(b"\n")

def receive_json():
    line = read_line().decode()
    json_start = line.find('{')
    return json.loads(line[json_start:])

def send_json(data):
    request = json.dumps(data).encode()
    connection.write(request)

connection = telnetlib.Telnet(server_host, server_port)
print(read_line())

detected_flag_length = 0
for length in range(1, 50):
    trial_data = [0] * length
    payload = json.loads(json.dumps({"option": "mix", "data": bytes(trial_data).hex()}))
    send_json(payload)

    mixed_value = receive_json()["mixed"]
    if validate_hash(mixed_value, length):
        detected_flag_length = length
        print("Detected flag length:", length)

trial_data = [0] * detected_flag_length
recovered_flag = 0
for bit_position in range(8 * detected_flag_length):
    trial_data[detected_flag_length - (bit_position // 8) - 1] = 1 << (bit_position % 8)
    payload = json.loads(json.dumps({"option": "mix", "data": bytes(trial_data).hex()}))
    send_json(payload)

    mixed_value = receive_json()["mixed"]
    if not validate_hash(mixed_value, detected_flag_length):
        recovered_flag += (1 << bit_position)
    trial_data[detected_flag_length - (bit_position // 8) - 1] = 0

print(long_to_bytes(recovered_flag))


# connects to a server and attempts to detetc the length of a flag by sending trail data and checking the hashes. 
# if the length is found, performs bit-by-bit recovery of the flag.