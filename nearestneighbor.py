import random
import matplotlib.pyplot
import time
from collections import deque
from ezutil_copy import Vec
from collections import defaultdict as dd
from itertools import permutations
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print '%r %2.2f sec' % \
              (method.__name__, te-ts)
        return result
    return timed

def dist(a,b):
    c=0
    for i in range(len(a)):
        c+=(a[i]-b[i])**2
    return c**.5

def raw_nn(k,ls):
    c = ls[0]
    d = dist(k,c)
    for a in ls:
        d2 = dist(a,k)
        if d2 < d:
            d,c=d2,a
    return Vec(*c)

def full_raw_nn(ks,ls):
    for k in ks:
        yield k,raw_nn(k,ls)

def sort_map(ls):
    d=len(ls[0])
    all_sorted = []
    #O(d*nlog(n))
    for i in range(d): #sort by each axis O(d)
        all_sorted.append(sorted(ls,key=lambda x:x[i])) 
    m={}
    #O(d*n)
    for j in range(len(ls)): 
        for i in range(d):
            srt=all_sorted[i]
            k=srt[j]
            if k in m:
                n=m[k]
            else:
                n=[None]*d
            if j>=len(ls)-1:
                n[i]=(srt[j-1],None)
            elif j<1:
                n[i]=(None,srt[j+1])
            else:
                n[i]=(srt[j-1],srt[j+1])
            m[k]=n
    return m

def sort_nn_help(k,ls,m):
    cl=random.choice(ls)
    cl_d = dist(k,cl)
    d=len(k)
    q=deque([cl])
    done = set()
    cnt=0
    while len(q) > 0:

        e = q.pop()
        if e in done:continue
        cnt+=1
        
        done.add(e)
        nei=m[e]
        for j in range(d): 
            lo,hi=nei[j] #Neighbors closest along jth axis, above and below.
            
            if lo and abs(lo[j]-k[j]) <= abs(e[j]-k[j]): #Closer along jth axis
                if (lo not in done):
                    q.append(lo)
                    d2 = dist(lo,k)

                    if d2 < cl_d:
                        cl,cl_d=lo,d2
                        # break

            if hi and abs(hi[j]-k[j]) <= abs(e[j]-k[j]): #Closer along jth axis
                if (hi not in done):
                    q.append(hi)
                    d2 = dist(hi,k)

                    if d2 < cl_d:
                        cl,cl_d=hi,d2
                        # break
    print cnt

    return cl

def sort_nn(ks,ls):
    s_map=sort_map(ls)
    for k in ks:
        yield k,sort_nn_help(k,ls,s_map)

def getData(d,sz,r=10):
    data=[]
    for i in xrange(sz):
        p = ()
        for j in range(d):
            p+=(random.uniform(-r,r),)
        data.append(p)
    return data

# O(n)
def gridify(ls,s=10.0):
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
            if f==2:
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


def all_face(dimen,dist):
    s=set()
    for d in range(dimen):
        for p in permutations(range(-dist, dist+1),dimen-1):
            a=list(p[:d])+[dist]+list(p[d:])

            if tuple(a) not in s:
                yield a
                s.add(tuple(a))
            a=list(p[:d])+[-dist]+list(p[d:])
            if tuple(a) not in s:
                yield a
                s.add(tuple(a))

def grid_nn(ks,ls): #map ks to ls
    gr,bx_sz=gridify(ls,s=20)
    for k in ks:
        yield k,find(gr,bx_sz,Vec(*k))


time_plot_test=1
verify_test=0
verify_plot=0
time_compare_test=0

dim=3

n=getData(dim,100)
m=getData(dim,1000)

@timeit
def s_test(n,m):
    for k,v in grid_nn(n,m):
        pass

if time_compare_test:
    s_test(n,m)

@timeit
def r_test(n,m):
    for k,v in full_raw_nn(n,m):
        pass

if time_compare_test:
    r_test(n,m)

if time_plot_test:
    m_data = getData(dim,2000,r=10) #going to map to n centers
    x=[]
    s_data=[]
    r_data=[]
    k=1
    for n in map(lambda x:int(1.7**x), range(10,22,1)): #cluster amount
        print n
        n_data = getData(dim,n,r=10)

        x.append(n)
        to=0
        for i in range(k):
            t = time.time()
            s_test(m_data,n_data)
            te=time.time()-t
            to+=te
        s_data.append(to/k)
        to=0
        for i in range(k):
            t = time.time()
            r_test(m_data,n_data)
            te=time.time()-t
            to+=te
        r_data.append(to/k)
        print

    matplotlib.pyplot.ylabel('seconds')
    matplotlib.pyplot.xlabel('centers')
    s,=matplotlib.pyplot.plot(x,s_data,c='r')
    u,=matplotlib.pyplot.plot(x,r_data,c='b')
    matplotlib.pyplot.legend([s, u],['spatial','naive'])
    matplotlib.pyplot.show()



if verify_test or verify_plot:
    for k,v in grid_nn(n,m):
        r = raw_nn(k,m) 
        if r != v:
            print r,v,r==v,r!=v
            if verify_plot:
                matplotlib.pyplot.plot(*zip(k,v),c='r')
                matplotlib.pyplot.plot(*zip(k,r),c='b')
            print 'fail'
            # break
    
    
if verify_plot:
    matplotlib.pyplot.show()

# s=set()
# for p in all_face(3,1):
#     if tuple(p) in s: continue
#     s.add(tuple(p))
#     print p,
# print '\n'
# for p in all_manhat(3,1):
#     print p,

