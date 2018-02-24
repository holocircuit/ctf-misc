import random

N = 200000
print(N)

for i in range(N):
    r = random.randrange(0, 200000000)
    print("%d %d" % (r, 2*r))
