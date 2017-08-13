

def n(a,k,x=0):
    if not x:x=a
    if not k:return x
    else:return n(a,k-1,(x+a/x)/2.0)

def square_root(k):
    s='"((%%(k)s+'+str(k)+'/%%(k)s)/2)"%%{"k":%s}';e=eval
    return e(e('s%('*9+'2'+')'*9))


def f(a):exec('a=(a+%s/a)/2;'%a*9+'print a')

f(10)