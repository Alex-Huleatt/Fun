#we're going to be in euclidean space.
#using euclidean distance

from ezutil_copy import Vec
from collections import defaultdict as dd

def dist(a,b):
    return sum([(a[i]-b[i])**2 for i in range(len(a))])**.5

# O(n)
def gridify(ls,s=10):

    mi,ma=ls[0],ls[0]
    for l in ls:
        mi=mi.cumumin(l)
        ma=ma.cumumax(l)

    box_size=(ma-mi)/s
    boxes=dd(list)
    for l in ls:
        index=(l).div_all(box_size).floor_all()
        boxes[index].append(l)

    return boxes, box_size

def find(gr,b_size,k):
    if len(gr.values()) == 0:
        return None
    k_index=k.div_all(b_size).floor_all()
    r=0
    d=len(k)
    c = None
    c_d = 0
    f=False
    while True: #worst case for data within the range of other data is O(1) (number of buckets)
        for p in all_manhat(d,r):
            t_index = k_index+Vec(*p)
            g=gr[t_index]
            for e in g: #O(n), but should O(log(n)) on disparate data
                e_d=dist(e,k)
                if c is None or e_d<c_d:
                    c,c_d=e,e_d
        if c is None:
            r+=1
        else:
            if f:
                return c
            else: #look one further out.
                f=True
                r+=1


    return None

def all_manhat(dimen,dist):
    def help(dim,dis): #memoize this
        if (dim,dis) in all_manhat.halpmemo:
            return all_manhat.halpmemo[(dim,dis)]
        if dim==1:
            return [[dis]]
        m=[]
        for i in range(dis+1): #dis**dimen?
            t=help(dim-1,dis-i)
            for tk in t:
                m.append([i]+tk)
        all_manhat.halpmemo[(dim,dis)]=m
        return m
    ls = help(dimen,dist)

    def h2(dimen): #produces list of len 2**dimen
        if dimen==1:
            yield [0];yield [1]
        else: 
            for d in h2(dimen-1):
                yield [0]+d;yield [1]+d

    #O(n*d*2**d)
    for l in ls: #O(m)
        for t in h2(dimen): #recalc, saves memory
            l_t=l[:]
            for i in range(dimen):
                if t[i]:
                    if l[i]==0:break #avoid duplicates
                    l_t[i]*=-1
            else:
                yield l_t
all_manhat.halpmemo={}

def grid_nn(ks,ls): #map ks to ls
    gr,bx_sz=gridify(ls)
    for k in ks:
        yield find(gr,bx_sz,k)



def test():

    ls=[
    [1,1],
    [0,0],
    [-1,-1],
    [-2,0]
    ]

    ls_vec=[Vec(*l) for l in ls]
    gr, b_size = gridify(ls_vec)
    toFind = Vec(*[-3,2])
    print find(gr,b_size, toFind)



if __name__ == '__main__':
    for dis in range(2,5):
        arr=[[0]*(2*dis+1) for i in range(dis*2+1)]
        for p in all_manhat(2,dis):
            arr[p[0]+dis][p[1]+dis]=1

        for r in arr:
            print r

        print '-------------------------'





