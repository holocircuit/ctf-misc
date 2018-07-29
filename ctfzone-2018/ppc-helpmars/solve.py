from hashlib import md5

def read_samples():
    s = open("mars_dna_samples.txt").read().strip().split("\n")

    l = []
    for sample in s:
        assert(sample.split(",")[0] == str(len(l)))

        l.append(sample.split(",")[1])
    return l

def best_solution(sol1, sol2):
    assert "".join(sol1) == "".join(sol2)

    if len(sol1) < len(sol2): return sol1
    if len(sol2) < len(sol1): return sol2

    for s1, s2 in zip(sol1, sol2):
        if len(s1) > len(s2): return sol1
        if len(s2) > len(s1): return sol2

    assert False
    return sol1


target = open("target.txt").read().strip().upper()

samples = read_samples()

# OK. We're given the condition that we want the solution which is the "longest" (in the lexicographic sense)
# We can dynamic program this.

samples = {sample : i for i, sample in enumerate(samples)}
best_solution_for_prefix = {0 : []}

for this_length in range(1, len(target) + 1):
    # Calculate the best solution for prefix of length i
    all_solutions = []

    for sol_length, solution in best_solution_for_prefix.items():
        rest = target[sol_length : this_length]
        if rest in samples:
            all_solutions.append(solution + [rest])

    print("[+] Found %d solutions for prefix length %d" % (len(all_solutions), this_length))

    if len(all_solutions) > 0:
        # Work out which is best according to the prefix rule
        solution = all_solutions[0]
        for i in range(1, len(all_solutions)):
            solution = best_solution(solution, all_solutions[i])

        best_solution_for_prefix[this_length] = solution
        print(solution)
        assert "".join(solution) == target[:this_length]

solution = best_solution_for_prefix[len(target)]
assert "".join(solution) == target

sol_string = ",".join(str(samples[sample]) for sample in solution)
print(sol_string)
print("ctfzone{%s}" % md5(sol_string.encode("ascii")).hexdigest())

