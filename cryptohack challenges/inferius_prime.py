from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD

x = 3
n = 742449129124467073921545687640895127535705902454369756401331
ct = 39207274348578481322317340648475596807303160111338236677373 
s = 752708788837165590355094155871
t = 986369682585281993933185289261

res = (s-1)*(t-1)

d = inverse(x,res)

a = pow(ct,d,n)
m = long_to_bytes(a)
print(m)

# factoring the modulus n to get prime numbers s & t then calculate Euler's totient.
# Cipher text is decrypted using pow() and converted back to the original message using long_to_bytes.