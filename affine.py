import math
alph = '~abcdefghijklmnopqrstuvwxyz'
def conv(st, a, b):
    k = ''
    for c in st:
        k += alph[(alph.find(c)*a+b) % 26]
    return k

#3,2 -> 9,8
a,b = 23,1
m = conv('foobar', a,b) 



def lcm(a,b):
    return abs(a*b)/gcd(a,b)

def gcd(a,b):
    while b != 0:
        a,b = b, a % b
    return a


a_n = lcm(a,26)
b_n = a_n * b - 26 * math.ceil(a/26)

print a_n, b_n