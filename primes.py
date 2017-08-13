import math

def gcd(a,b):
    c,d = max(a,b), min(a,b)

    if (c,d) in gcd.stored:
        return gcd.stored[(c,d)]

    while b != 0: 
        a, b = b, a % b

    gcd.stored[(c,d)] = a
    return a
gcd.stored = {}


def primes(n):
    for i in range(min(n,len(primes.ls))):
        yield primes.ls[i]
    for i in range(len(primes.ls)+1, n):
        k = primes.ls[-1] + 2
        j, p = 0, 2
        while p ** 2 <= k:
            p = primes.ls[j]
            if k % p == 0:
                j = 0
                k += 2
                continue
            j += 1
        primes.ls.append(k)
        
        yield k
primes.ls = [2,3,5,7,11,13,17,19]


def primefact(n):
    k = 1
    for p in primes(n):
        k*=p
    return k

def factorize(n):

    def sub(s):
        k = 1
        for p in primes(s):
            if p ** 2 > s:
                break
            else:
                k *= p
        g = gcd(s,k)
        return g

    sm = []
    while n != 1:
        s = sub(n)
        
        if s == 1:
            break

        sm.append(s)

        n //= s
    sm.append(n)
    return sm


# all([n%x for x in range(n**.5+1)])
