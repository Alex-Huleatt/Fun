import ez
from ez import Circle
import random, math

my_win = ez.Win(show_fps=True) #create a window, display the fps.

def up(**kwargs):
	for p in particles:
		p.update(gravities)

def mag(p1):
	return (p1[0]**2 + p1[1]**2)**(1.0/2)

def normalVec(p1, p2):
	c = (p2[0]-p1[0], p2[1]-p1[1])
	mg = mag(c)
	return (c[0]/mg, c[1]/mg)
def diff(p1, p2):
	return (p1[0]-p2[0], p1[1]-p2[1])

min_dis = 10
class particle():

	def __init__(self, x=0, y=0, vx=0, vy=0, m = 20.0):
		self.x=x
		self.y=y
		self.vx=vx
		self.vy=vy
		self.prevx = x
		self.prevy = y
		self.m = m
		self.c = ez.Circle(x=x,y=y,width=5,color=(1,0,0,1), stroke=5)

	def g_force(self, x):
		return self.m / x**2

	def update(self, forces=[]):
		fx,fy = 0,0
		for f in forces:
			if f == self:
				continue
			oldm = mag(diff((f.x, f.y), (self.prevx, self.prevy)))
			nowm = mag(diff((f.x, f.y), (self.x, self.y)))
			if nowm < min_dis or oldm < min_dis:
				continue
			def gAtTime(t):
				pos = (self.prevx + self.vx * t, self.prevy + self.vy*t)
				d = mag(diff((f.x,f.y), pos))
				return f.g_force(d) 

			fmag = quadrature(gAtTime, 0, 1)
			fdir = normalVec((f.x,f.y), (self.x, self.y))

			
			fx+=fdir[0]*fmag
			fy+=fdir[1]*fmag
		self.vx -= fx
		self.vy -= fy
		self.prevx = self.x
		self.prevy = self.y
		self.x += self.vx
		self.y += self.vy

	def render(self):
		self.c.x = self.x
		self.c.y = self.y
		self.c.render()

#gaussian quadrature, integral approximation
def quadrature(f, a ,b):
	consts = [(0.6521451548625461,-0.3399810435848563), (0.6521451548625461,0.3399810435848563),
			 (0.3478548451374538,-0.8611363115940526),(0.3478548451374538,0.8611363115940526)]
	c1 = b-a
	c2 = (b+a)/2.0
	s = 0
	for k in consts:
		s += k[0]*f(c1/2 * k[1] + c2)
	res = c1/2.0 * s
	return res


particles = []
gravities = []


vCoeff = 0
for i in range(50):
	p = particle(x=my_win.width*random.random(),y=my_win.height*random.random(), vx=random.random()*vCoeff -.5*vCoeff, vy=random.random()*vCoeff - .5*vCoeff)
	particles.append(p)
	my_win.add(p)
	gravities.append(p)

my_win.tock=up #set update callback (called 60times or whatever FPS is set to.)

ez.runWin() #run everything

# def f(x):
# 	return 1

#print quadrature(f, -1, 0)
