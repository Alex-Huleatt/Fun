s=open('panda.txt').read().split('\n')
a,b=len(s),max([len(c) for c in s])
r,t,m=[[' ']*b for i in'.'*a],[' ','\n'],[-1,1,0,0]
for i,j in[(i,j)for i in range(len(s))for j in range(len(s[i]))]:
    if s[i][j]not in t and sum([1 for k,l in zip(m,m[::-1])if i+k<a and j+l<len(s[i+k])and s[i+k][j+l]not in t])!=4:r[i][j]='*'
print '\n'.join(map(''.join,r))
