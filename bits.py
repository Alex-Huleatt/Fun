from PIL import Image
from random import shuffle,sample
import sys
import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print '%r %2.2f sec' % \
              (method.__name__, te-ts)
        return result
    return timed

#---------------------------grid nn code-------------
from ezutil_copy import Vec
from collections import defaultdict as dd
def gridify(ls,s=1.0):
    ls_2=[]
    mi=Vec(*ls[0])
    ma=mi
    for l in ls:
        v=Vec(*l)
        ls_2.append(v)
        mi=mi.cumumin(v)
        ma=ma.cumumax(v)

    box_size=(ma-mi)/s
    boxes=dd(list)
    for l in ls_2:
        index=(l).div_all(box_size).floor_all()
        boxes[index].append(l)

    return boxes, box_size

# @timeit
def find(gr,b_size,k):
    if len(gr.values()) == 0:
        return None
    k_index=k.div_all(b_size).floor_all()
    r=0
    d=len(k)
    c = None
    c_d = 0
    f=0
    while True: #worst case for data *within the range of other data* is O(1) (number of buckets)
        for p in all_manhat(d,r):
            t_index = k_index+Vec(*p)
            g=gr[t_index]
            for e in g: #O(n), but should O(log(n)) or something on uniform-y data
                e_d=dist(e,k)
                if c is None or e_d<c_d:
                    c,c_d=e,e_d
        if c is None:
            r+=1
        else:
            if f==0:
                return c
            else: #look one further out.
                f+=1
                r+=1
    return None


'''this is one weird-ass function'''
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

    def h2(dimen): #produces list of len 2**dimen
        if dimen==1:
            yield [0];yield [1]
        else: 
            for d in h2(dimen-1):
                yield [0]+d;yield [1]+d

    ls = help(dimen,dist)
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
    print 'gridify-ing'
    gr,bx_sz=gridify(ls,s=20)
    print '\tgridified'
    for k in ks:
        yield k,find(gr,bx_sz,Vec(*k))

#-------------------------------------------------------------------

def dist(a,b):
    r_bar = (a[0]+b[0])/2.0
    dr,dg,db=a[0]-b[0],a[1]-b[1],a[2]-b[2]
    return ((2+r_bar/256.0)*dr**2+4*dg**2+(2+(255-r_bar)/256.0*db**2)) #uh

# ks can be a generator
def NNs(ks,ls):
    dists={}
    for i in xrange(len(ls)): #O(n**2)
        a=ls[i]
        for j in xrange(i+1,len(ls)):
            b=ls[j]
            d=dist(a,b)
            dists[(a,b)],dists[(b,a)]=d,d
    memo={}
    for k in ks: #O(mn)
        if k in memo:
            yield memo[k]
            continue
        nn=ls[0]
        d=dist(k,nn)
        for n in ls[1:]:
            if dists[(n,nn)] < 2*d:
                d2=dist(k,n)
                if d2<d:
                    nn,d=n,d2
        memo[k]=nn
        yield nn

def closest(k, ls, shuff=True):
    ls_s=ls[:]
    if shuff:shuffle(ls_s) #handle non-unique centers.
    c=ls_s[0]
    cc=dist(k,c)
    for n in ls_s:
        d=dist(k,n)
        if d<cc:c,cc=n,d
    return c,cc

def furthest_from_all(possible, ls):
    fur,fur_c=None,0
    p_s=sample(possible,20)
    for p in p_s:
        s=0
        for k in ls:
            s+=dist(p,k)
        if s>fur_c:
            fur,fur_c=p,s
    return fur,fur_c


def kmeans2(z,k,avg_f):
    print 'kmeans'
    ls=z.keys()
    def init_centroids():
        print 'initializing centroids'
        cen=[Vec(*ls[0])]
        for i in xrange(k-1):
            p,_=furthest_from_all(ls,cen)
            cen.append(Vec(*p))
        print '\tinitialized'
        return cen

    #initialize centroids
    centroids=init_centroids()
    print 'initialized centroids.'
    while True: 
        new_cent=[Vec(0,0,0) for i in range(k)]
        counts=Vec(*([0]*k))
        for s,c in grid_nn(ls,centroids):
            idx=centroids.index(c)
            new_cent[idx]+=s*z[s]
            counts[idx]+=z[s]

        for j in range(k): #k
            if counts[j]!=0:
                new_cent[j]/=counts[j]

        if len(set(centroids)^set(new_cent))==0: #k
            break

        centroids=new_cent

    return centroids

def compress(px,sz,fname):
    avg = lambda ls:[float(k)/len(ls) for k in map(sum,zip(*ls))]
    h,w=sz
    nw=Image.new('RGB',(h,w),'black')
    rpx=nw.load()
    S = 30 #chunks
    k = 4 #total colors S^2*k
    n=0
    total = []
    for i in range(S):
        for j in range(S):
            print n
            low=(i*h/S,j*w/S)
            hi=(min((i+1)*h/S,h), min(w,(j+1)*w/S))
            z={}
            for r in xrange(low[0],hi[0]):
                for c in xrange(low[1],hi[1]):
                    p=px[r,c]
                    if p in z:z[p]+=1
                    else:z[p]=1
            total.extend(kmeans2(z,k,avg))
            n+=1

    def k_gen():
        for i in xrange(w):
            for j in xrange(h):
                yield px[j,i]

    #total = [(255,255,255),(50,100,50)]
    c=0
    s=set()
    for nn in grid_nn(k_gen(),total):
        rpx[c%h,c//h]=tuple(nn)
        s.add(nn)
        if not c % 20000:
            print c
        c+=1 
    nw.save('%s.png'%fname)
    return s

input_file = sys.argv[1]
out_name=sys.argv[2]
rl = Image.open(input_file)
px=rl.load()
# s=set()
# for i in range(rl.size[0]):
#     for j in range(rl.size[1]):
#         s.add(px[i,j])
# print len(s)
total=compress(px,rl.size,out_name)
print len(total), total
