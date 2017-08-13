#!/usr/bin/env python
import sys
def e(c):
 u,b,i,v,s='[{<(',dict,0,0,e.s
 z=b(zip(u,']}>)'))
 while i<len(c):
  k=c[i];h=k in z
  if h and c[i+1]==z[k]:exec b(zip(u,['v+=x','v+=s[e.a].pop()if s[e.a]else 0','e.a=1-e.a','v+=1']))[k]
  elif h:
   n,y=0,i
   while c[:i+1].count(k)>c[:i+1].count(z[k]):i+=1
   r=c[y+1:i]
   if k!='{':n=e(r)
   exec b(zip(u,['n=-n','while s[e.a]and s[e.a][-1]:v+=e(r)','n','s[e.a]+=[n]']))[k]
   v+=n
  i+=1
 return v
e.s,e.a=[map(int,sys.argv[2:]),[]],0
e(sys.argv[1])
for s in e.s[e.a]:print s