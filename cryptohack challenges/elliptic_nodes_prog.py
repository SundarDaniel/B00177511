from Crypto.Util.number import inverse,bytes_to_long, long_to_bytes

def cusp_solver(G,H,p):
    M = Integers(p)
    i = M(G[1])//M(G[0]) 
    j = M(H[1])//M(H[0]) 
    return discrete_log(j, i)
def node_solver(G,H,p,a):
    R = Integers(p)
    u = R(G[1]-a*G[0])//R(G[1]+a*G[0])
    v = R(H[1]-a*H[0])//R(H[1]+a*H[0])
    return discrete_log(v, u)

p = 4368590184733545720227961182704359358435747188309319510520316493183539079703
g = [8742397231329873984594235438374590234800923467289367269837473862487362482, 225987949353410341392975247044711665782695329311463646299187580326445253608]
A = [2582928974243465355371953056699793745022552378548418288211138499777818633265, 2421683573446497972507172385881793260176370025964652384676141384239699096612]

a = ((g[1]**2) - (A[1]**2) - (g[0]**3) + (A[0]**3))//Integers(p)(g[0] - A[0])
b = (g[1]**2) - (g[0]**3) - (a*g[0])

P.<x,y> = PolynomialRing(GF(p))
p = (x^3 + a*x + b)
na = 0
if len(p.factor()) == 1:
    na = cusp_solver(g,A,p)
if len(p.factor()) == 2:
    singular_pt = p.factor()[0][0].coefficient({x:0}) + p.factor()[1][0].coefficient({x:0})
    if p.factor()[0][1] == 2:
        singular_pt -= 2*p.factor()[0][0].coefficient({x:0})
        g[0] += p.factor()[0][0].coefficient({x:0})
        A[0] += p.factor()[0][0].coefficient({x:0})
    else:
        singular_pt -= 2*p.factor()[1][0].coefficient({x:0})
        g[0] += p.factor()[1][0].coefficient({x:0})
        A[0] += p.factor()[1][0].coefficient({x:0})
    singular_pt = GF(p)(singular_pt).square_root()
    na = node_solver(g,A,p,singular_pt)

print(na, long_to_bytes(na))

# first calculates the curve parameters a & b and check factoriztion of the polynomial p. Based on p,
# it finds the logarithm. Finally, it gives the output as both a number and its byte representation.