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

def modular_exponentiation_solver(base, result, modulus, totient, factors):
    Ring = Integers(modulus)
    generator = Ring(base)
    values = [0] * len(factors)
    for idx, (prime, exponent) in enumerate(factors):
        for exp in range(exponent):
            coefficient = bsgs(generator**(totient // prime), (result // generator**values[idx])**(totient // prime**(exp + 1)), (0, prime))
            values[idx] += coefficient * (prime**exp)
    return crt(values, [prime**exponent for prime, exponent in factors])

def validate_padding(data):
    padding = data[-data[-1]:]
    return all(padding[i] == len(padding) for i in range(len(padding)))

def decrypt_message(secret, initialization_vector, encrypted_data):
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    aes_key = sha1.digest()[:16]
    encrypted_data = bytes.fromhex(encrypted_data)
    initialization_vector = bytes.fromhex(initialization_vector)
    cipher = AES.new(aes_key, AES.MODE_CBC, initialization_vector)
    plaintext = cipher.decrypt(encrypted_data)
    if validate_padding(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

server_host = "socket.cryptohack.org"
server_port = 13378

def read_line():
    return connection.read_until(b"\n")

def receive_json():
    line = read_line().decode()
    start_idx = line.find('{')
    return json.loads(line[start_idx:])

def send_json(payload):
    request = json.dumps(payload).encode()
    connection.write(request)

upper_limit = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633918
secondary_limit = 782447372963237017080911425690626808320121477344046500785903911140548592900614218375169986555497769722994612768766237489225391319847998034333635622999777018085492552042629201517236242969387773417387518064509930154467125225099893166734205067493594146299578427161129003066430095422159690004313302195831114109968070664752615603031826096360561083674123245084443411780282892018035180938429828776626215527562796692413033621528951604797200401283355182471258495210998412729835889355808886300

prime_factors = []
current_prime = 1
highest_prime = 1
while len(prime_factors) < 3:
    product = 2
    temp_prime = current_prime
    while len(prime_factors) < 3 and product < secondary_limit:
        product *= temp_prime
        temp_prime = next_prime(temp_prime)
        if is_prime(product + 1):
            if product + 1 > upper_limit:
                prime_factors.append(product + 1)
    highest_prime = max(highest_prime, temp_prime)
    current_prime += 1

total_product = 1
totient_product = 1
for prime in prime_factors:
    total_product *= prime
    totient_product *= (prime - 1)

remaining_totient = totient_product
prime_count = 2
factorization = []
while remaining_totient > 1:
    exponent = 0
    while remaining_totient % prime_count == 0:
        remaining_totient //= prime_count
        exponent += 1
    if exponent != 0:
        factorization.append([prime_count, exponent])
    prime_count = next_prime(prime_count)

ring = Integers(total_product)
generator = ring(2)
factors = [[prime, exponent] for prime, exponent in factorization]
temp_totient = totient_product
for idx in range(len(factors)):
    while factors[idx][1] > 0 and generator**temp_totient == 1:
        factors[idx][1] -= 1
        temp_totient //= factors[idx][0]
    if generator**temp_totient != 1:
        factors[idx][1] += 1
        temp_totient *= factors[idx][0]

discrete_logs = []
for prime in prime_factors:
    connection = telnetlib.Telnet(server_host, server_port)
    alice_data = receive_json()
    bob_data = receive_json()
    encrypted_data = receive_json()
    test_data = '''{"p": "0x1", "g": "0x2", "A": "0x2232"}'''
    altered_data = json.loads(test_data)
    altered_data['p'] = hex(prime)
    send_json(altered_data)
    bob_received = receive_json()
    encrypted_received = receive_json()
    discrete_logs.append((int(bob_received["B"], 0)))
while len(discrete_logs) != len(prime_factors):
    prime_factors.pop()
computed_secret = crt(discrete_logs, prime_factors)
ring = Integers(total_product)
generator = ring(2)
final_secret = modular_exponentiation_solver(ring(2), ring(computed_secret), total_product, temp_totient, factors)
finite_field = GF(alice_data["p"])
generator_ff = finite_field(alice_data["g"])
alice_key = finite_field(alice_data["A"])
bob_key = finite_field(bob_data["B"])
if generator_ff**final_secret == bob_key:
    shared_key = alice_key**final_secret
    print(decrypt_message(shared_key, encrypted_data['iv'], encrypted_data['encrypted']))
else:
    print(final_secret)

# it connects to a remote server to implement Diffie hellman key exchange to get a secret.
# it uses modular exponentiation, CRT and discrete logarithms to compute the secret, then decrypts a flag using aes.