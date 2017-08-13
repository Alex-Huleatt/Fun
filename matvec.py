arr=list(input())

print [reduce(lambda a,b:a+(b[0]*b[1]),[0]+zip(arr[i:]+arr[:i],arr)) for i in range(len(arr))]
