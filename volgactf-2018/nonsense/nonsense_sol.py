import hashlib
import os

# DSA parameters
g = 88125476599184486094790650278890368754888757655708027167453919435240304366395317529470831972495061725782138055221217302201589783769854366885231779596493602609634987052252863192229681106120745605931395095346012008056087730365567429009621913663891364224332141824100071928803984724198563312854816667719924760795
y = 18433140630820275907539488836516835408779542939919052226997023049612786224410259583219376467254099629677919271852380455772458762645735404211432242965871926570632297310903219184400775850110990886397212284518923292433738871549404880989194321082225561448101852260505727288411231941413212099434438610673556403084
p = 89884656743115795425395461605176038709311877189759878663122975144592708970495081723016152663257074178905267744494172937616748015651504839967430700901664125135185879852143653824715409554960402343311756382635207838848036159350785779959423221882215217326708017212309285537596191495074550701770862125817284985959
q = 1118817215266473099401489299835945027713635248219

# parameters for the random generator
a = 3437776292996777467976657547577967657547
b = 828669865469592426262363475477574643634

signatures = [['VolgaCTF{nKpV/dmkBeQ0n9Mz0g9eGQ==}', 1030409245884476193717141088285092765299686864672, 830067187231135666416948244755306407163838542785],
              ['VolgaCTF{KtetaQ4YT8PhTL3O4vsfDg==}', 403903893160663712713225718481237860747338118174, 803753330562964683180744246754284061126230157465],
              ['VolgaCTF{8NXrNihQFZHXN/aLQeYKtg==}', 573204611556272128788136170196175308321188191436, 91103585122319085944642441222968347176761155259],
              ['VolgaCTF{uDh3jKDKW2utTkblP43NQw==}', 988208923601321592314278832250352152086708201148, 535902494423594375360085340272213659149931817732],
              ['VolgaCTF{gtE4LCuhT5drcDunvKz/oQ==}', 398664332680411743333343859695363011153860369916, 392831307484494740050270232580899453387203218646],
              ['VolgaCTF{rS9IEsyvXHOCUo0/TL2c1A==}', 1069308776596602518230279648695605679674084062212, 1092197517441497735860968374670599451237193808469],
              ['VolgaCTF{4gEh/j9EGwZ20NEoBieDbQ==}', 299126738734367538949359921058714964192219834697, 1033663138335940105270395993670462206279669465530],
              ['VolgaCTF{RwpewhJhMGH0MORFtXQfAw==}', 45947153576235029841784762518202071246619636555, 160232137675713914067049553022084774145041067326],
              ['VolgaCTF{i7QjVusEQboUz2tPx/Uxkw==}', 158481243947457932495342738131507924205209157088, 260728631055453998945003114392349125641429319965],
              ['VolgaCTF{nQwf/+78QMObu3S3Oh1Olg==}', 117030185689896730023482874167356847173848413476, 645757721193000290408806214518814010431656731046]]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# for testing.
class DSA():
	def __init__(self, x):
		self.g = g
		self.y = pow(g, x, p)
		self.p = p
		self.q = q
		self.x = x

	def sign(self, m, k):
		h = int(hashlib.md5(m).hexdigest(), 16)
		r = pow(self.g, k, self.p) % self.q
		s = int(((self.x * r + h) * modinv(k, self.q)) % self.q)
		return (r, s)

	def verify(self, m, r, s):
		if 0 < r and r < self.q and 0 < s and s < self.q:
			h = int(hashlib.md5(m).hexdigest(), 16)
			w = modinv(s, self.q)
			u1 = (h * w) % self.q
			u2 = (r * w) % self.q
			v = ((pow(self.g, u1, self.p) * pow(self.y, u2, self.p)) % self.p) % self.q
			return v == r
		return None
class LCG():
	def __init__(self, seed):
		self.a = a
		self.b = b
                
		self.m = q
		self.seed = seed
		self.state = (self.a * self.seed + self.b) % self.m

	def next_number(self):
		self.state = (self.a * self.state + self.b) % self.m
		return self.state

# For the random number generator, we can calculate coefficients a_i, b_i such that
# x_i = a_i*seed + b_i
def calculate_random_generator_parameters(n):
    # suppose we have (a_i, b_i)
    # then x_{i+1} = a*x_i + b = a*(a_i)*seed + (a*b_i + b)
    # initial internal state has (a_1, b_1) = (a, b)

    (x, y) = (a, b)
    for _ in xrange(n+1):
        x = (x * a) % q
        y = (a * y + b) % q
    return (x, y)

# if we have two signatures, we can then solve for the seed:
# suppose k_1 = x_1*seed + y_1, k_2 = x_2*seed + y_2
# we have
# x*r_1 = k_1*s_1 - H_1
# x*r_2 = k_2*s_2 - H_2
# dividing gives a rational function of the seed and stuff we know:
# (r1/r2)*(x_2*seed + b2) - H_2 = (x_1*seed + y_1) - H_1
# we can then rearrange to find the seed

# some testing to show this works
def test():
    seed = 10
    x = 20
    generator = LCG(seed)
    signature = DSA(x)

    l = []
    for _ in range(2):
        message = "VolgaCTF{" + os.urandom(16).encode('hex') + "}"
        k = generator.next_number()
        print k
        (r, s) = signature.sign(message, k)
        l.append((message, r, s))

    (message1, r1, s1) = l[0]
    (message2, r2, s2) = l[1]
    (x1, y1) = calculate_random_generator_parameters(0)
    (x2, y2) = calculate_random_generator_parameters(1)
    h1 = int(hashlib.md5(message1).hexdigest(), 16)
    h2 = int(hashlib.md5(message2).hexdigest(), 16)

    # use these for sanity checking, but obviously we don't know the seed
    k1 = (x1*seed + y1) % q
    k2 = (x2*seed + y2) % q

    # assert the basic relations
    assert (x*r1 - k1*s1 + h1) % q == 0
    assert (x*r2 - k2*s2 + h2) % q == 0

    # assert dividing out x works
    lhs = r1 * (s2*(x2 * seed + y2) - h2)
    rhs = r2 * (s1*(x1 * seed + y1) - h1)
    assert (lhs - rhs) % q == 0

    # assert that we can rewrite to solve for the seed
    linear = (r1*s2*x2 - r2*s1*x1)
    constant = r2*(s1*y1 - h1) - r1*(s2*y2 - h2)
    assert (linear*seed - constant) % q == 0
    soln = (constant * modinv(linear, q)) % q
    assert soln == seed


def solve_for_seed(msg1, msg2, n1, n2):
    # n1, n2 are the numbers for the generators
    (m1, r1, s1) = msg1
    (m2, r2, s2) = msg2
    h1 = int(hashlib.md5(m1).hexdigest(), 16)
    h2 = int(hashlib.md5(m2).hexdigest(), 16)

    (x1, y1) = calculate_random_generator_parameters(n1)
    (x2, y2) = calculate_random_generator_parameters(n2)

    linear = (r1*s2*x2 - r2*s1*x1) % q
    constant = (r2*(s1*y1 - h1) - r1*(s2*y2 - h2)) % q
    soln = (constant * modinv(linear, q)) % q
    return soln

seed = solve_for_seed(signatures[0], signatures[1], 0, 1)

# yay! now solve for x
(msg, r, s) = signatures[0]
h = int(hashlib.md5(msg).hexdigest(), 16)
(x1, y1) = calculate_random_generator_parameters(0)
k = x1*seed + y1

x = (((k*s) - h) * modinv(r, q)) % q
print x
print pow(g, x, p)
print y
print hex(x)
