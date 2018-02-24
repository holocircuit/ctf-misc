N = 2000
W = 1800

print("%d %d" % (N, W))
import random
for i in range(N):
    print("%d %d" % (random.randrange(1, 20000), random.randrange(1, 2000)))
