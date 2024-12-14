from sage.all import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

import gmpy2
from Cryptodome.Util import number
from itertools import combinations

def read_data():
    result = {'n': [], 'c': []}
    with open("output.txt", 'rb') as file:
        while True:
            line = file.readline()
            if not line: break
            line = line.strip().decode()
            if not line: continue

            key, value = line.split('=')
            key = key.strip()
            if key == 'e':
                continue
            result[key].append(int(value))

    return result

def rsa_decrypt(data, exponent):
    for group in combinations(zip(data['n'], data['c']), exponent):
        modulus_product = 1
        for item in group: modulus_product *= item[0]

        combined_message = 0
        for item in group:
            combined_message += item[1] * number.inverse(modulus_product // item[0], item[0]) * (modulus_product // item[0])
        combined_message %= modulus_product
        message, is_exact = gmpy2.iroot(combined_message, exponent)
        if is_exact:
            print(number.long_to_bytes(message))

data = read_data()
rsa_decrypt(data, 3)


# performs a cryptographic operation using CRT. It then attempts to decrypt the message by combining ciphertexts and moduli in combinations and solving using modular inverse.
# If a valid message is found, it prints the decrypted message as bytes.