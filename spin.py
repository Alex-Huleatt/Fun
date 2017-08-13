import time,sys
# s=[u'\u2014','/','|','\\']
# for i in xrange(50000000):
#     print '\r',
#     for j in range(1,100):
#         print s[(i//j//3)%len(s)],
#     sys.stdout.flush()
#     time.sleep(.001)



s2=':3 meow!'
for i in xrange(5000000):
    print '\r',' '*(i%100) + s2,
    sys.stdout.flush()
    time.sleep(.05)
