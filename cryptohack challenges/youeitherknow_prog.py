secret = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
t = bytes.fromhex(secret)
k = b'myXORkey'
[print(chr(k[i%len(k)]^v),end='') for i,v in enumerate(t)]

# the input is in hexadecimal format and it converts into bytes. 
# iterates through each byte of the secret, XORs each byte with a corresponding byte from key and gives result.
# output is the result of applying XOR encryption to the message using key, effectively decrypting it.