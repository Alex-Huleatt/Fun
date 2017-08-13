import statistics

def partition(ls,k=0):
    if k == len(ls[0]):
        return ls
    med=statistics.median(map(lambda a:a[k], ls))
    l,r=[],[]
    for e in ls:
        if e[k]<med:l+=[e]
        else:r+=[e]
    return med,partition(l,k=k+1), partition(r,k=k+1)

def dist(a,b):
    return sum(map(lambda x,y:(x-y)**2,a,b))


def raw_nn(fro,to):
    for f in fro:
        n =to[0]
        d = dist(f,n)
        for t in to:
            d2 = dist(f,t)
            if d2 < d:
                d=d2
                n=t
        yield f,n

def geomap(pts):
    geo={}
    for a in pts:
        geo[a]=[]
        for b in pts:
            if b==a:continue
            geo[a]+=[b]
    geo2={}
    for a in geo.keys():
        new_edges=[]
        for b in geo[a]:
            d = dist(a,b)
            for c in geo[a]:
                if b==c:continue
                if dist(a,c) + dist(c,b) < 2*d:
                    break
            else:
                new_edges.append(b)
        geo[a]=new_edges
    return geo


def geoNN(fro, to):
    g = geomap(to)
    print 'map created.'
    print g
    for a in fro:
        n=g.keys()[0]
        while True:
            d=dist(a,n)
            for k in g[n]:
                d2=dist(a,k)
                if d2<d:
                    n=k
                    break
            else:
                break
        yield a,n
