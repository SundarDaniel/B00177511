def mi(a, p):

    t, new_t = 0, 1
    r, new_r = p, a

    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    if r > 1:
        raise ValueError(f"{a} has no inverse modulo {p}")
    if t < 0:
        t += p

    return t

a = 3
p = 13
inverse = mi(a, p)
print(f"The multiplicative inverse of {a} modulo {p} is {inverse}.")

# It uses extended euclidean algorithm to calculate multiplicative inverse. It iteratively update the values
# to find inverse.