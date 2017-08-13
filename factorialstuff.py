import time,sys

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result
    return timed

def next_prime():
    def is_prime(k):
        for p in next_prime.s:
            if not k%p:
                return False
            if p**2>k:
                return True
    ns=next_prime.s
    k=ns[-1]
    while True:
        k+=2
        if is_prime(k):
            ns.append(k)
            return k
next_prime.s=[2,3,5,7,11]

def primes(n=-1,till=-1):
    i=0
    while True:
        p=next_prime.s[i]
        if (till!=-1 and p>till) or (n!=-1 and i==n):
            break
        yield p
        i+=1
        if i==len(next_prime.s):
            for j in range(100):next_prime()

count=0
def primefact(k):
    def v(z):
        i,n=1,0
        global count
        while k/(z**i): #O(log(k))
            n+=k/(z**i)
            i+=1
            count+=1
        return n
    for p in primes(till=k):
        yield (p,v(p))

'''
normal for-loop factorial
'''
@timeit
def factorial(n):
    c=1
    for i in xrange(1,n+1):c*=i
    return c

@timeit
def factorialR(hi):
    def factorialR_help(hi,lo):
        r=hi-lo
        if hi-lo<1000:
            c=1
            for i in xrange(lo,hi+1):c*=i
            return c
        else:
            return factorialR_help(lo+r/2,lo)*factorialR_help(hi,lo+r/2+1)
    return factorialR_help(hi,1)

def prod_rec(ls):
    if len(ls)==0:
        return 1
    if len(ls)==1:
        return ls[0][0]**ls[0][1]
    return prod_rec(ls[:len(ls)/2])*prod_rec(ls[len(ls)/2:])

def modexp ( g, u, p ):
   """computes s = (g ^ u) mod p
      args are base, exponent, modulus
      (see Bruce Schneier's book, _Applied Cryptography_ p. 244)"""
   s = 1
   while u != 0:
      if u & 1:
         s = (s * g)%p
      u >>= 1
      g = (g * g)%p;
   return s


@timeit
def wilsons(p):
    return factorialR(p-1)%p==p-1
    
@timeit
def trial(p):
    for k in primes():
        if k**2 > p:
            return True
        if not p%k:
            return False


p=67280421310721
# trial(p)
wilsons(p)