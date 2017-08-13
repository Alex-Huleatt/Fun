from collections import defaultdict


class ntree():
    def __init__(self, dim,v=None):
        self.dim=2
        self.ls=[None]*2**dim
        self.root=v

    def add(self,k):
        k2=ntree(self.dim,k)
        if self.root is None:
            self.root=k
        else:
            n = self
            while True:
                idx=reduce(lambda x,y:(int(y)^(x<<1)),map(lambda x,y:bool(x<y),n.root,k)) #waow
                if n.ls[idx]==None:
                    n.ls[idx]=k2
                    return
                else:
                    n=n.ls[idx]

    # def find(self, k):
    #     if self.root is None:
    #         return None
    #     else:
    #         n=self
    #         closest = self.root
    #         while True:
    #             idx=reduce(lambda x,y:(int(y)^(x<<1)),map(lambda x,y:bool(x<y),n.root,k)) #waow
    #             if n.ls[idx]==None:
    #                 return closest
    #             else:
    #                 if 
    #                 n=n.ls[idx]


    def inorder(self):
        for k in self.ls:
            if k is None:
                continue
            for k2 in k.inorder():
                yield k2
        yield self.root

    def __str__(self):
        return str(self.root)
    __repr__=__str__

#all neighbors on a grid.
#includes input point.
def neighbors(p,dim=1):
    if dim==1:
        return [(p[0]+1,), (p[0]-1,), (p[0],)]
    else:
        ls=[]
        r,n = neighbors((p[0],)),neighbors(p[1:],dim-1)
        for c in r:
            for k in n:
                ls.append(c+k)
        return ls

def orthoneighbors(p):
    ls = []
    p_ls = list(p)
    for k in range(len(p)):
        t = p_ls[:]
        t[k]+=1
        ls.append(tuple(t))
        t[k]-=2
        ls.append(tuple(t))
    return ls

def count(nt):
    d = defaultdict(int)
    for p in nt.inorder():
        on = orthoneighbors(p)
        for n in on:
            if n != p:
                d[n]+=1
    return d


nt = ntree(dim=2)

nt.add((0,0))

nt.add((-1,0))
nt.add((0,1)) 
for n in nt.inorder():
    print n


    



