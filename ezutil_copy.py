import math

class Vec():

	def __init__(self, *args):
		self._ls = []
		for a in args:
			self._ls.append(float(a))

	def __getitem__(self, key):
		return self._ls[key]

	def __setitem__(self, key, value):
		self._ls[key] = value

	def __add__(self, other):
		return Vec(*[self[i]+other[i] for i in range(len(self))])

	__radd__ = __add__

	def __neg__(self):
		return Vec(*[-1*k for k in self])

	def __sub__(self, other):
		return Vec(*[self[i]-other[i] for i in range(len(self))])

	def __mul__(self, num):
		return Vec(*[self[i]*num for i in range(len(self))])

	__rmul__=__mul__

	def __div__(self, num):
		return Vec(*[self[i]/num for i in range(len(self))])

	def __str__(self):
		return str(self._ls)

	__repr__=__str__

	def __iter__(self):
		for k in self._ls:
			yield k

	def __eq__(self,other):
		return self._ls==other._ls

	def __ne__(self,other):
		return not self==other

	def __hash__(self):
		return tuple([k for k in self]).__hash__()

	def __len__(self):
		return len(self._ls)

	def copy(self):
		return Vec(*self)

	def index(self, k):
		for i in range(len(self._ls)):
			if self._ls[i]==k:
				return i
		return -1

	def mag(self):
		return sum([k**2 for k in self])**.5

	def dot(self, other):
		return sum(self[i]*other[i] for i in range(len(self)))

	def scalar_project(self, other):
		return self.dot(other) / other.mag()

	def vector_project(self, other):
		return other * self.scalar_project(other)

	def rotate_origin2D(self, rad):
		c = self.mag()
		theta = math.atan(self[1]/self[0])
		new_x = math.cos(theta + rad) / c
		new_y = math.sin(theta + rad) / c
		return Vec([new_x, new_y])

	def mul_all(self, other):
		return Vec(*[self[i]*other[i] for i in range(len(self))])

	def div_all(self, other):
		return Vec(*[self[i]/other[i] for i in range(len(self))])

	def extend(self, *args):
		for a in args:
			self._ls.append(a)

	def less_than(self, other):
		return map(lambda x,y:bool(x<y),self,other)

	def cumumin(self, other):
		return Vec(*[min(self[i],other[i]) for i in range(len(self))])
	def cumumax(self, other):
		return Vec(*[max(self[i],other[i]) for i in range(len(self))])

	def floor_all(self):

		v=Vec(*[int(self[i]) for i in range(len(self))])
		for i in range(len(v)):
			v[i]=int(v[i])
		return v

class Mat():
	
	def __init__(self, args):
		self._ls = []
		for a in args:
			self._ls.append(Vec(*a))

	def row(self, n):
		return Vec(zip(self._ls)[n])

	def col(self, n):
		return Vec(self._ls[n])

	def __mul__(self, n):
		return Mat([k*n for k in self])

	__rmul__=__mul__

	def __add__(self, other):
		return Mat([self[i]+other[i] for i in range(len(self))])

	def __getitem__(self, k):
		return self._ls[k]

	def __setitem__(self, k, v):
		self._ls[k]=Vec(*v)

	def __len__(self):
		return len(self._ls)

	def __str__(self):
		return '\n'.join([str(k) for k in self._ls])

	__repr__=__str__

	def rref(self):
		ls = self._ls[:]
		i,j=0,0
		while i < len(self):
			if zip(*ls)[j]==0:
				j+=1
				continue

			if ls[i][j] == 0:
				for k in range(len(ls)):
					if ls[k][j] != 0:
						ls[i],ls[k]=ls[k],ls[i]
						break

			ls[i] = ls[i]/ls[i][j]

			for k in range(len(ls)):
				if k != i:
					ls[k] = ls[k]-ls[i]*ls[k][j]/ls[i][j]
			i+=1;j+=1

		return Mat(ls)

	def transpose(self):
		return Mat(zip(*self._ls))

	def matmul(self, other):
		return Mat((lambda a,b:[[sum(map(lambda x,y:x*y,r,c))for c in zip(*b)]for r in a])(self._ls, other._ls))

	@staticmethod
	def identity(N):
		return Mat([[0]*i+[1]+[0]*(N-i-1) for i in range(N)])

	@staticmethod
	def zero(N,M=0):
		if not M:
			M = N
		return Mat([[0]*M for k in range(N)])

	def LU(self):
		m = len(self)

		def P():
			ident = Mat.identity(m)
			for j in range(m):
				row = max(xrange(j, m), key=lambda i: abs(self[i][j]))
				if j != row:
					ident[j], ident[row] = ident[row], ident[j]
			return ident
                                                                                                                                                                                                                
		L,U = Mat.zero(m),Mat.zero(m)

		# Create the pivot matrix P and the multipled matrix PA                                                                                                                                                                                            
		P = P()
		PA = P.matmul(self)

		# Perform the LU Decomposition                                                                                                                                                                                                                     
		for j in xrange(m):                                                                                                                                                                                                
			L[j][j] = 1.0
                                                                                                                                                                                    
			for i in xrange(j+1):
				s1 = sum(U[k][j] * L[i][k] for k in xrange(i))
				U[i][j] = PA[i][j] - s1
                                                                                                                                                                 
			for i in xrange(j, m):
				s2 = sum(U[k][j] * L[i][k] for k in xrange(j))
				L[i][j] = (PA[i][j] - s2) / U[j][j]

		return (P, L, U)

	def det(self):
		P,L,U = self.LU()
		n = len(self)
		s = 0
		hit=set([])
		for i in range(n):
			if i in hit:
				continue
			k = P[i].index(1)
			c = 1
			hit.add(i)
			while k!=i:
				c+=1
				k=P[k].index(1)
				hit.add(k)

			s+=1*(c%2)

		det = (-1)**s
		for i in range(n):
			det*=L[i][i]*U[i][i]
		return det

	def aug(self, other):
		c = []
		for i in range(len(self)):
			v = self[i].copy()
			v.extend(*other[i])
			c.append(v)
		return Mat(c)

	def deaug(self, n):
		c = []
		for i in range(len(self)):
			k = self[i][n:]
			c.append(k)
		return Mat(c)

	def inverse(self):
		return self.aug(Mat.identity(len(self))).rref().deaug(len(self[0]))

class Ntree():
    def __init__(self, dim,v=None):
        self.dim=2
        self.ls=[None]*2**dim
        self.root=v

    def add(self,k):
        k2=Ntree(self.dim,k)
        if self.root is None:
            self.root=k
        else:
            n = self
            while True:
                idx=reduce(lambda x,y:(int(y)^(x<<1)),n.root.less_than(k)) #waow
                if n.ls[idx]==None:
                    n.ls[idx]=k2
                    return
                else:
                    n=n.ls[idx]

    


    def inorder(self):
        for k in self.ls:
            if k is None:continue
            for k2 in k.inorder():yield k2
        yield self.root

    def __str__(self):
        return str(self.root)
    __repr__=__str__


if __name__=='__main__':
	v1=Vec(1,2,3)
	v2=Vec(*[1,2,3])
	print v1==v2