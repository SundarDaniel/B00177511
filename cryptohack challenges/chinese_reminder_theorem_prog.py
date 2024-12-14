N = 935
mod1 = 5
mod2 = 11
mod3 = 17

n1 = N / mod1 
n2 = N / mod2 
n3 = N / mod3 

e1 = 561
e2 = 595
e3 = 715

x = 2 * e1 + 3 * e2 + 5 * e3

print("FLAG =", x % N)

# First it calculates n1, n2 & n3 then computes a weighted sum and finally prints the remainder.