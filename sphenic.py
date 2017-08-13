(lambda n:reduce(lambda a,b:a*b,range(1,n))%n==n-1)




def s(n):a,k=2,0;exec('k+=1-bool(n%a)\nwhile not n%a:n/=a;k+=10**9\na+=1\n'*n);return k==3*10**9+3

for i in range(100):
    if s(i):
        print i