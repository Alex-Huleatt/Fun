

def m(s,u,d):
    return map(lambda x:s[:x].count(u)-s[:x].count(d),range(len(s)+1))

s,u,d='((()))','(',')'
i=1
while s[:i].count(u)-s[:i].count(d):i+=1

print i