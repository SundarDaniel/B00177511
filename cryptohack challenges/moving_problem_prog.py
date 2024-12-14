from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def flag_decrypt(shared_secret: int, iv: str, ct: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    k = sha1.digest()[:16]
    ct = bytes.fromhex(ct)
    iv = bytes.fromhex(iv)
    cipher = AES.new(k, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)

    if padded(pt):
        return unpad(pt, 16).decode('ascii')
    else:
        return pt.decode('ascii')

shared_secret = secret
iv = "eac58c26203c04f68d63dc2c58d79aca"
ciphertext = 'bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d'

print(flag_decrypt(shared_secret, iv, ciphertext))
# aes using cbc mode implemented in this code. It generates k by hashing 
# then decrypts the ciphertext with key and initialization vector.
# after decryption, it checks padding and removes padding to get the original message.