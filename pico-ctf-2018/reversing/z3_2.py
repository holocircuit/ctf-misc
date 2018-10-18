#!/usr/bin/python2

from hashlib import sha512
from z3 import *
import sys

def solve_chalbox(chalbox):
    print chalbox
    length, gates, check = chalbox
    s = Solver()
    
    gates = gates
    
    b = IntVector("b", length + len(gates))

    for i in xrange(length + len(gates)):
      s.add(b[i] >= 0)
      s.add(b[i] <= 1)

    for i, (name, args) in enumerate(gates):
        print name, args
  
        if name == "true":
            s.add(b[length + i] == 1)
            continue

        b1 = b[args[0][0]] 
        b2 = b[args[1][0]] 
        target = b[length + i]
   
        if args[0][1]:
          u1 = 1-b1
        else:
          u1 = b1

        if args[1][1]:
          u2 = 1-b2
        else:
          u2 = b2

        if name == "xor":
            s.add(Xor(u1 == 1, u2 == 1) == (target == 1))
        elif name == "or":
            s.add(Or(u1 == 1, u2 == 1) == (target == 1))
  
        """
        elif name == "or":
            if args[0][1] and args[1][1]:
                s.add(u1 == 0 or u2 == 0)
            elif args[0][1] and not args[1][1]:
                s.add(u1 == 0 or u2 == 1)
            elif args[1][1] and not args[0][1]:
                s.add(u1 == 1 or u2 == 0)
            elif (not args[1][1]) and (not args[0][1]):
                s.add(u1 == 1 or u2 == 1)
        """
        print i, s.check()

    s.add(Xor(b[check[0]] == 1, check[1]))
    s.check()
    model = s.model()

    print model[b[check[0]]]
    print check[1]
 
    l = []
    for i in xrange(length + len(gates)):
      l.append(int(str(model[b[i]])))
    return l

def verify_soln(soln, chalbox):
    length, gates, check = chalbox

    for i, (name, args) in enumerate(gates):
        print i
 
        j = i + length
        b = soln[j]
        if name == 'true':
            assert b == 1
        else:
            u1 = soln[args[0][0]] ^ args[0][1]
            u2 = soln[args[1][0]] ^ args[1][1]
            if name == 'or':
                assert b == (u1 | u2)
            elif name == 'xor':
                assert b == (u1 ^ u2)

    print soln[check[0]]
    print check[1]
    assert soln[check[0]] ^ check[1]

with open("map2.txt", 'r') as f:
    cipher, chalbox = eval(f.read())

l = solve_chalbox(chalbox)
verify_soln(l, chalbox)
print int("".join(str(x) for x in l[:chalbox[0]])[::-1], 2)
