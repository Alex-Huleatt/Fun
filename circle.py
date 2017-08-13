
def circle(x,y,z): #find circle w/ 3 points
    i,a=complex,abs
    x,y,z=i(*x),i(*y),i(*z)
    w=(z-x)/(y-x)
    c=(x-y)*(w-a(w)**2)/2j/w.imag-x
    return (a(c.real),a(c.imag)),a(c+x)

def csr(m):
    s,b=sum(m,[]),len(m[0])
    return[filter(bool,s),[0]+[sum(map(bool,s[:b+k*b]))for k in range(b)],[i%b for i,v in enumerate(s)if v]]

m=lambda a,b:[[sum(map(lambda x,y:x*y,r,c))for c in zip(*b)]for r in a] #matrix mult
f=lambda n:reduce(lambda a,b:a*b,[1]+range(1,n+1)) #factorial
c=lambda n,k:f(n)/(f(k)*f(n-k)) #choose
p=lambda n:[1]+[c(n,i)for i in range(1,n+1)] #pascal's triangle
w=lambda *k:sum(zip(*k),()) #interweave


# mat = [[0,0,0,0],[5,8,0,0],[0,0,3,0],[0,6,0,0]]
# print csr(mat)

# x = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
# y = [[1,2],[1,2],[3,4]]

# print m(x,y)

print w('111','222','333')

