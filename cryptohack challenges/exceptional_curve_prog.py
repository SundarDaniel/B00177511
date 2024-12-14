from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def padding(msg):
    pad = msg[-msg[-1]:]
    return all(pad[i] == len(pad) for i in range(0, len(pad)))


def flag_decryption(shared_secret: int, iv: str, ct: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    k = sha1.digest()[:16]
    # Decrypt flag
    ct = bytes.fromhex(ct)
    iv = bytes.fromhex(iv)
    cipher = AES.new(k, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)

    if padding(pt):
        return unpad(pt, 16).decode('ascii')
    else:
        return pt.decode('ascii')


shared_secret = secret
iv = "719700b2470525781cc844db1febd994"
ct = "335470f413c225b705db2e930b9d460d3947b3836059fb890b044e46cbb343f0"

print(flag_decryption(shared_secret, iv, ct))

# key derived from secret using sha1. It hashes secret to obtain new key and uses iv to decrypt.
# After decrypting, it checks for valid padding and removes it to give the original message.