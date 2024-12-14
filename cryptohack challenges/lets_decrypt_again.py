from Crypto.Util.number import bytes_to_long, long_to_bytes
import socket
import json
from sage.all import *
import hashlib
import re
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, inverse, isPrime
from pkcs1 import emsa_pkcs1_v15
import sympy
import random

ADDRESS_PATTERN = re.compile("^Please send all my money to ([1-9A-HJ-NP-Za-km-z]+)$")

def validate_address(message):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    address = ADDRESS_PATTERN.match(message)
    if not address:
        return False
    address = address.group(1)
    raw_bytes = b"\0" * (len(address) - len(address.lstrip(alphabet[0])))
    result = 0
    for char in address:
        result *= 58
        result += alphabet.index(char)
    raw_bytes += long_to_bytes(result)

    if len(raw_bytes) != 25:
        return False
    if raw_bytes[0] not in [0, 5]:
        return False
    return raw_bytes[-4:] == hashlib.sha256(hashlib.sha256(raw_bytes[:-4]).digest()).digest()[:4]

VALID_PATTERNS = [
    re.compile(r"^This is a test(.*)for a fake signature.$").match,
    re.compile(r"^My name is ([a-zA-Z\s]+) and I own CryptoHack.org$").match,
    validate_address
]

KEY_LENGTH = 768

SERVER_HOST = "socket.cryptohack.org"
SERVER_PORT = 13394

socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def read_response():
    return socket_connection.recv(1024).decode("utf-8")

def receive_json():
    response = read_response()
    json_start = response.find('{')
    return json.loads(response[json_start:])

def send_json(data):
    request = json.dumps(data).encode()
    socket_connection.sendall(request)

BTC_SAMPLES = []
with open("./btc_samples.txt", "r") as file:
    for line in file:
        BTC_SAMPLES.append(line.strip())

def generate_test_patterns():
    alphabet = " ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    patterns_0, patterns_1, patterns_2 = [], [], []

    for address in BTC_SAMPLES:
        patterns_2.append(b"Please send all my money to " + address.encode("utf-8"))
    for char in alphabet:
        patterns_1.append(b"My name is " + char.encode("utf-8") + b" and I own CryptoHack.org")
        patterns_0.append(b"This is a test " + char.encode("utf-8") + b" for a fake signature.")

    return [patterns_0, patterns_1, patterns_2]

def request_signature():
    send_json({"option": "get_signature"})
    return receive_json()

def set_public_key(public_key):
    send_json({"option": "set_pubkey", "pubkey": public_key})
    return receive_json()

def claim_message(message, exponent, index):
    send_json({"option": "claim", "msg": message.decode(), "e": exponent, "index": index})
    return receive_json()

def validate_message(message, index, modulus, exponent, suffix, signature):
    if not (0 <= index < len(VALID_PATTERNS)):
        return False

    if not message.endswith(suffix):
        return False

    encoded_message = emsa_pkcs1_v15.encode(message, KEY_LENGTH // 8)
    computed_signature = pow(signature, exponent, modulus)

    if bytes_to_long(encoded_message) == computed_signature:
        return bool(VALID_PATTERNS[index](message[:-len(suffix)].decode()))
    else:
        return False

def combine_factors(factor_dict, factors):
    combined = factor_dict
    for prime, exp in factors:
        if prime in combined:
            combined[prime] += exp
        else:
            combined[prime] = exp
    return combined

def find_b_smooth_prime(bound):
    product = 2
    prime_factors = []
    while True:
        test_prime = sympy.randprime(0, bound)
        exp = random.randint(1, 10)
        prime_factors.append([test_prime, exp])
        product *= test_prime**exp
        if is_prime(product + 1):
            return [product + 1, product, prime_factors]

def generate_pohlig_hellman_modulus(base, bit_size):
    smooth_bound = 1 << 10
    modulus, field_order, factors = 1, 1, {}
    while modulus.bit_length() < bit_size:
        prime = find_b_smooth_prime(smooth_bound)
        if prime[0].bit_length() < bit_size and prime[0] != -1 and gcd(base, prime[0]) == 1:
            modulus *= prime[0]
            field_order *= prime[1]
            factors = combine_factors(factors, prime[2])
    return [modulus, field_order, factors]

def solve_pohlig_hellman(target, base, modulus, field_order, factors):
    mod_ring = IntegerModRing(modulus)
    generator = mod_ring(base)
    value = mod_ring(target)
    solutions = []
    for prime, exp in factors.items():
        prime_exp = prime**exp
        sub_generator = generator**(field_order // prime_exp)
        sub_value = value**(field_order // prime_exp)
        solutions.append(discrete_log(sub_value, sub_generator, ord=prime_exp))
    return CRT(solutions, [prime**exp for prime, exp in factors.items()])

def validate_all_messages(signature):
    global test_patterns
    test_patterns = generate_test_patterns()
    result_count = 0

    modulus, field_order, factors = generate_pohlig_hellman_modulus(signature, 800)
    response = set_public_key(hex(modulus))

    if response['status'] != 'ok':
        return False

    suffix = response['suffix'].encode()
    for index, pattern_group in enumerate(test_patterns):
        valid_messages = []
        for test_message in pattern_group:
            full_message = test_message + suffix
            encoded_message = emsa_pkcs1_v15.encode(full_message, KEY_LENGTH // 8)
            try:
                exponent = solve_pohlig_hellman(bytes_to_long(encoded_message), signature, modulus, field_order, factors)
            except:
                continue

            if validate_message(full_message, index, modulus, exponent, suffix, signature):
                valid_messages.append([full_message, exponent])

        if valid_messages:
            result_count += 1

    return result_count == 3

def retrieve_flag():
    xor_value = 0
    for index, valid_message_group in enumerate(test_patterns):
        response = claim_message(valid_message_group[0][0], hex(valid_message_group[0][1]), str(index))
        if response['msg'] == "Congratulations, here's a secret":
            xor_value ^= int(response['secret'][2:], 16)
        else:
            return
    print("Flag:", xor_value.to_bytes((xor_value.bit_length() + 7) // 8, byteorder='big'))

attempts = 0
while True:
    attempts += 1
    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_connection.connect((SERVER_HOST, SERVER_PORT))

    read_response()
    response = request_signature()
    signature_value = int(response['signature'][2:], 16)

    if validate_all_messages(signature_value):
        retrieve_flag()
        socket_connection.close()
        break

    socket_connection.close()
    print("Retrying... (Attempt:", attempts, ")")


# code connects to a remote server and interacts with it to perform cryptographic operations.
# It generates test patterns, then attempts to validate and solve the signature challenge.
# Finally, it obtains flag by correctly identifying and validating messages.