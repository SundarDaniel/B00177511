def euclid_gcd(x, y):
    if x < y:
        return euclid_gcd(y, x)

    while y != 0:
        (x, y) = (y, x % y)

    print("\n[+] GCD: {}".format(x))
    return x


a = 66528
b = 52920

euclid_gcd(a, b)

# Uses Euclidean algoritm to compute gcd. It checks x > y by swapping values if necessary, then modulo operation is applied 
# iteratively to reduce the numbers until y becomes zero. The final x value is GCD.