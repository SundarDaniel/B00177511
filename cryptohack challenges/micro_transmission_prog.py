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
iv = "ceb34a8c174d77136455971f08641cc5"
ct = "b503bf04df71cfbd3f464aec2083e9b79c825803a4d4a43697889ad29eb75453"

print(flag_decryption(shared_secret, iv, ct))

# this code decrypts a given ciphertext using AES in CBC mode. Hashes the secret with SHA-1 to generate aes key.
# then uses new key with iv to decrypt the cipher text. Finally, it checks padding and returns the original message.