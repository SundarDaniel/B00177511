def is_quadratic_residue(x, p):
    for i in range(p):
        if (i * i) % p == x % p:
            return i
    return None

p = 29
t = [14, 6, 20]

qs = None
sr = None

for x in t:
    root = is_quadratic_residue(x, p)
    if root is not None:
        qs = x
        sr = min(root, p - root)
        break

print(f"The quadratic residue is {qs}.")
print(f"The smaller square root of {qs} modulo {p} is {sr}.")

# uses extended euclidean algorithm to compute multiplicative inverse. It iteratively calculates gcd and coeffients which express the inverse of a modulo 0.
# if the gcd=1 returns inverse otherwise error.