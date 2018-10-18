from z3 import *

def chr2(x):
    x = int(repr(x))
    if x <= 10: return chr(ord("0") + x)
    return chr(0x41 + x - 10)

solver = Solver()
key = IntVector("key", 16)

for i in xrange(16): 
    solver.add(key[i] >= 0)
    solver.add(key[i] < 36)

# constraint1
solver.add((key[0] + key[1]) % 0x24 == 0xe)

# constraint2
solver.add((key[2] + key[3]) % 0x24 == 0x18)

# constraint3
solver.add((key[2] - key[0]) % 0x24 == 0x6)

# constraint4
solver.add((key[1] + key[3] + key[5]) % 0x24 == 0x4)

# constraint5
solver.add((key[2] + key[4] + key[6]) % 0x24 == 0xd)

# constraint6
solver.add((key[3] + key[4] + key[5]) % 0x24 == 0x16)

# constraint7
solver.add((key[6] + key[8] + key[10]) % 0x24 == 0x1f)

# constraint8
solver.add((key[1] + key[4] + key[7]) % 0x24 == 0x7)

# constraint9
solver.add((key[9] + key[12] + key[15]) % 0x24 == 0x14)

# constraint10
solver.add((key[13] + key[14] + key[15]) % 0x24 == 0xc)

# constraint11
solver.add((key[8] + key[9] + key[10]) % 0x24 == 0x1b)

# constraint12
solver.add((key[7] + key[12] + key[13]) % 0x24 == 0x17)

print solver.check()

model = solver.model()

print "".join(chr2(model[key[i]]) for i in xrange(16))
