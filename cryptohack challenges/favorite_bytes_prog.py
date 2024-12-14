secret = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'
from pwn import xor
for i in range(256):
    flag = xor(bytes.fromhex(secret),i)
    if b'crypto{' in flag:
        print(flag)

# it uses xor function from the pwn library. It checks whether the result contains the string in each iteration.
# if the correct key is identified, it prints the decrypted message.