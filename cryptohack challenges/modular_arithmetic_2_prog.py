p1 = 17
p2 = 65537

print("3^17 mod 17 =", pow(3, 17, p1))
print("5^17 mod 17 =", pow(5, 17, p1))
print("7^16 mod 17 =", pow(7, 16, p1))

b = 273246787654
e = 65536
m = p2

r = pow(b, e, m)
print(f"273246787654 ^ 65536 mod 65537 = {r}")

# It demonstrates modular exponentiation using pow function. This operation is commonly used in cryptography.