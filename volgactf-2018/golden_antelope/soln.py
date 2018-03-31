# Some parameters
import os

def H(state):
    return int("".join(map(str, state[-1:-9:-1])), 2)

class Generator:
    def __init__(self, state):
        self.state = state

    def next_state(self, idxs):
        self.idxs = idxs
        y = 0
        for i in self.idxs:
            y ^= self.state[i]
        out = self.state[31]
        for i in range(31, 0, -1):
            self.state[i] = self.state[i - 1]
        self.state[0] = y

L = [0xf1, 0xef, 0x29, 0xbe, 0xb8, 0xf6, 0x4f, 0xaf, 0xb2, 0x92, 0xe3, 0xfc, 0xc6, 0x72, 0x48, 0xc3,
     0xbf, 0xa0, 0x10, 0xd1, 0x23, 0x34, 0x0c, 0x07, 0x7c, 0xf8, 0xae, 0xe8, 0xc9, 0xe1, 0x38, 0x36,
     0x4c, 0x2c, 0x0b, 0x70, 0x7b, 0xe7, 0xd7, 0xc5, 0xac, 0x57, 0xab, 0xd5, 0x4b, 0x77, 0xa5, 0xce,
     0xee, 0xf4, 0x47, 0x25, 0x8a, 0xf3, 0xfd, 0xbb, 0x5c, 0xe0, 0x2a, 0x19, 0x5d, 0xeb, 0xa6, 0x81,
     0x12, 0x61, 0x59, 0xcf, 0xc8, 0xa8, 0xfe, 0x3e, 0x31, 0x1e, 0x46, 0x7e, 0x3d, 0xd0, 0x3c, 0xc7,
     0xdc, 0x33, 0x8f, 0xca, 0x78, 0x6f, 0x0d, 0x62, 0x9d, 0xd9, 0x89, 0x73, 0x8c, 0x4e, 0xb7, 0xc0,
     0x03, 0x56, 0xb9, 0x79, 0x75, 0xda, 0x6e, 0x1c, 0xff, 0x67, 0x2f, 0xbc, 0x69, 0x91, 0x2b, 0x9b,
     0x7f, 0x17, 0x01, 0xde, 0xfa, 0x4a, 0x02, 0x0e, 0x8b, 0xa9, 0x58, 0x2d, 0xd8, 0xf9, 0x3b, 0xb3, 
     0x49, 0x65, 0xcc, 0xa3, 0xbd, 0x16, 0x21, 0xd3, 0xe5, 0xd6, 0x42, 0x60, 0x4d, 0x20, 0x97, 0x5e, 
     0x2e, 0xe9, 0x18, 0xc2, 0x63, 0x64, 0xf5, 0x6a, 0xd2, 0x68, 0x1b, 0x1f, 0xc4, 0xea, 0x74, 0xa2, 
     0x45, 0x82, 0xb6, 0x32, 0x84, 0xed, 0x50, 0x26, 0xcb, 0x5f, 0x37, 0xa1, 0x15, 0xa4, 0x51, 0x53, 
     0xb4, 0x09, 0xaa, 0x1a, 0x14, 0x43, 0xba, 0xdf, 0x87, 0x66, 0x85, 0x52, 0x3a, 0x28, 0x9a, 0xb1, 
     0x44, 0x9f, 0x96, 0x41, 0xdd, 0x86, 0x88, 0x9e, 0x71, 0xb0, 0x13, 0x98, 0xe4, 0x05, 0xf7, 0x6c, 
     0xb5, 0x93, 0x8e, 0x55, 0xec, 0x8d, 0xf2, 0x6d, 0x9c, 0xa7, 0xad, 0x00, 0x08, 0xf0, 0xe6, 0x6b, 
     0x7a, 0xcd, 0xfb, 0x80, 0x0a, 0x83, 0x27, 0x39, 0x30, 0x06, 0x76, 0x90, 0x94, 0x35, 0x54, 0x04, 
     0x0f, 0xc1, 0x5b, 0x99, 0x11, 0x40, 0x5a, 0xd4, 0xe2, 0x95, 0x3f, 0x22, 0x7d, 0x24, 0x1d, 0xdb]
# M = L_inverse
M = [L.index(i) for i in range(256)] 
X = [0, 4, 5, 8, 9, 10, 13, 15, 17, 18, 27, 31]
A0 = [0, 1, 3, 4, 6, 7, 9, 10, 11, 15, 21, 22, 25, 31]
A1 = [0, 1, 6, 7, 8, 9, 10, 12, 16, 21, 22, 23, 24, 25, 26, 31]
B = [0, 2, 5, 14, 15, 19, 20, 30, 31]
range_max = 256

def n_to_bits(n):
    return map(int, list(bin(n)[2:].zfill(32)))

# RX = Generator(map(int, list(bin(int(os.urandom(4).encode('hex'), 16))[2:].zfill(32))))
# RA = Generator(map(int, list(bin(int(os.urandom(4).encode('hex'), 16))[2:].zfill(32))))
# RB = Generator(map(int, list(bin(int(os.urandom(4).encode('hex'), 16))[2:].zfill(32))))

def tap_generators(RX, RA, RB):
    RX.next_state(X)
    if RX.state[29] == 0:
        RA.next_state(A0)
    else:
        RA.next_state(A1)
    if RX.state[26] == 0:
        RB.next_state(B)
    else:
        RB.next_state(B)
        RB.next_state(B)

def get_number(x, a, b):
    return (x + L[a] + L[b]) % 256

def get_number_from_states(RX, RA, RB):
    return get_number(H(RX.state), H(RA.state), H(RB.state))

def get_number_from_user():
    return int(raw_input("[-] Need another number...: "))

# Let's define a "pre-state" as the last 8 bits. The output of the generators is purely defined by the pre-state.
# We can do a reasonable brute force (through 2 of the generators) to get all possible pre-states resulting in a given bit
def possible_prestates_one_forward((x, a, b)):
    # tapping twice depends on bit 26 (= -6) of x. However, this is after it's tapped. So we actually need to check bit 25 here.
    # and note that we're reading this such that right is the high bit, so bit 25 is the 2nd lowest bit
    tap_b_twice = (x & 2) != 0
    x = (x << 1) % 256
    a = (a << 1) % 256
    b = (b << (2 if tap_b_twice else 1)) % 256

    return set((x_, a_, b_) for x_ in xrange(x, x+2) for a_ in xrange(a, a+2) for b_ in xrange(b, b + 4 if tap_b_twice else b+2))

def get_all_possible_prestates_generating_bit(n, previous_prestates = None):
    l = []
    for x in xrange(256):
        for a in xrange(256):
            b = M[(n - L[a] - x) % 256]
            l.append((x, a, b))

    possible_prestates = set(l)

    if previous_prestates == None:
        return possible_prestates

    possible_prestates_derived_from_previous_possible_states = set(x for prestate in previous_prestates for x in possible_prestates_one_forward(prestate))
    possible_prestates.intersection_update(possible_prestates_derived_from_previous_possible_states)
    return possible_prestates

print "[+] Starting step 0..."
n = get_number_from_user()

# Step 0: Tap the first time. Brute-force through X, A to get all possible pre-states
possible_prestates = get_all_possible_prestates_generating_bit(n)

print "[+] Starting step 1..."
# Step 1: Tap until we're down to 1 possible state. This should take around 4 moves.
for _ in range(10):
    n = get_number_from_user()

    possible_prestates = get_all_possible_prestates_generating_bit(n, possible_prestates)

    if len(possible_prestates) == 1:
        break
    print "[+] Number of possible prestates for this round:", len(possible_prestates)

print "[+] Starting step 2"
# Step 2: Tap 24 more times, store the possible prestates for each one. (Same method as above.) Should be 1, maybe 2 possibilities for each one.
prestates = {}
prestates[0] = possible_prestates

for run in xrange(1, 25):
    n = get_number_from_user()

    possible_prestates = get_all_possible_prestates_generating_bit(n, possible_prestates)

    # print information about what the next possible number would be, to give ourselves a bit more room
    # this isn't used in the main loop at all
    print "[+] Guess one of these numbers: ", set(get_number(x, a, b) for prestate in possible_prestates for (x, a, b) in possible_prestates_one_forward(prestate))

    prestates[run] = possible_prestates

# Step 3: Work backwards to the run we got in Step 1. We should have all of X, A. B is a bit more complicated.
# Specifically, for run (24-i), we should have all the possibilities for the last (8+i) bits
# needs a name. let's call it "partial knowledge form"
def one_prestate_to_dictionary(n):
    d = {}
    for i in xrange(-8, 0):
        d[i] = n % 2
        n /= 2
    return d

def shift_dictionary_back(d, i):
    return {n - i : c for n, c in d.iteritems()}

def combine_and_check_consistency(d1, d2):
    d = {}
    keys = d1.keys() + d2.keys()

    for key in keys:
        if key in d1 and key in d2:
            if d1[key] != d2[key]:
                return None
            d[key] = d1[key]
        elif key in d1:
            d[key] = d1[key]
        elif key in d2:
            d[key] = d2[key]
        else:
            assert False

    return d

def prestates_to_partial_knowledge_form(prestates, partial_knowledge_for_next_run = None):
    # Just from the prestate
    from_prestate = [(one_prestate_to_dictionary(x), one_prestate_to_dictionary(a), one_prestate_to_dictionary(b)) for (x, a, b) in prestates]

    if partial_knowledge_for_next_run == None:
        return from_prestate


    # From the next run
    from_next_run = []
    for (x, a, b) in partial_knowledge_for_next_run:
        tap_b_twice = x[-6] == 1
        x = shift_dictionary_back(x, 1)
        a = shift_dictionary_back(a, 1)
        b = shift_dictionary_back(b, 2 if tap_b_twice else 1)
        from_next_run.append((x, a, b))

    # Combine from_prestate and from_next_run
    results = []

    for (x1, a1, b1) in from_prestate:
        for (x2, a2, b2) in from_next_run:
            x = combine_and_check_consistency(x1, x2)
            a = combine_and_check_consistency(a1, a2)
            b = combine_and_check_consistency(b1, b2)
            if x != None and a != None and b != None:
                results.append((x, a, b))

    return results

run_to_partial_state_knowledge = {}
run_to_partial_state_knowledge[24] = prestates_to_partial_knowledge_form(prestates[24])

for run in xrange(23, -1, -1):
    run_to_partial_state_knowledge[run] = prestates_to_partial_knowledge_form(prestates[run], run_to_partial_state_knowledge[run + 1])

# Step 4: At this point, we should have the state for that step!
# Create generators, generate stream from there
if len(run_to_partial_state_knowledge[0]) != 1:
    print("Warning: We found multiple possible states. I'm going to pick one arbitrarily. It might be wrong.")

(x, a, b) = list(run_to_partial_state_knowledge[0])[0]
x = [x[i] for i in xrange(-32, 0)]
a = [a[i] for i in xrange(-32, 0)]
b = [b[i] for i in xrange(-32, 0)]

RX_mine = Generator(x)
RA_mine = Generator(a)
RB_mine = Generator(b)

for _ in range(24):
    tap_generators(RX_mine, RA_mine, RB_mine)

for _ in range(150):
    tap_generators(RX_mine, RA_mine, RB_mine)
    print "[+] Next number:", get_number_from_states(RX_mine, RA_mine, RB_mine)
