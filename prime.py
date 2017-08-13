def factorial(n):
    c=1
    for i in xrange(1,n+1):
        c*=i
    return c

def factorialRec(hi,lo):
    r=hi-lo
    if hi-lo < 100:
        c=1
        for i in xrange(lo,hi+1):
            c*=i
        return c
    else:
        return factorialRec(lo+r/2,lo)*factorialRec(hi,lo+r/2+1)


def next_prime():
    ns=next_prime.s
    k=ns[-1]
    while True:
        k+=2
        for n in ns:
            if not k%n:
                break
        else:
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

def factorize(k):
    ls=[]
    for p in primes():
        if not k%p:
            c = 0
            while not k%p:
                k/=p
                c+=1
            ls.append((p,c))
        if k==1:break
    return ls

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

    return [(p,v(p)) for p in primes(till=k)]


def prod_rec(ls):
    if len(ls)==0:
        return 1
    if len(ls)==1:
        return ls[0][0]**ls[0][1]
    return prod_rec(ls[:len(ls)/2])*prod_rec(ls[len(ls)/2:])

def prod_iter(ls):
    c=1
    for k in ls:
        c*=k[0]**k[1]
    return c
k=100000
# factorial(k)
factorialRec(k,1)
# print 'primes done',len(next_prime.s)
# primefact(k)