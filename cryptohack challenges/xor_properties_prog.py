k1 = 0xa6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
k2 = 0x37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e ^ k1
k3 = 0xc1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1 ^ k2

FLAG = 0x04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf ^ k1 ^ k3 ^ k2

print(bytes.fromhex(hex(FLAG)[2:]))

# it performs a series of bitwise XOR operations between three keys and a value.
# flag is calculated by XOR-ing an initial hex value and then result is converted into byte.