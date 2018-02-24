NW = input()
N = int(NW.split(" ")[0])
W = int(NW.split(" ")[1])

hackers = []
for _ in range(N):
    s = input()
    skill = int(s.split(" ")[0])
    weight = int(s.split(" ")[1])
    hackers.append((skill, weight))

# d will contain map from weight -> best skill you can do with exactly that weight
# enforcing that only keys at most W are in the dictionary

d = {0:0}

# add hacker
for i, (next_skill, next_weight) in enumerate(hackers):
    # early exit (the program suggests the weight can be way more than we have space for)
    if next_weight > W: continue

    old_dict = d.copy()
    for total_weight, total_skill in old_dict.items():
        weight_with_this_hacker = total_weight + next_weight
        skill_with_this_hacker = total_skill + next_skill

        # early exit if the weight is too much
        if weight_with_this_hacker <= W:
            if weight_with_this_hacker in d:
                d[weight_with_this_hacker] = max(d[weight_with_this_hacker], skill_with_this_hacker)
            else:
                d[weight_with_this_hacker] = skill_with_this_hacker

print(max(d.values()))
