def get_all_digit_chars():
    l = []
    for i in range(0x110000):
        if chr(i).isdigit():
            l.append(i)
    return l

alldigits = get_all_digit_chars()
target = 2365552391
target -= (2406-ord("0"))*1000000
target -= (57-ord("0"))*100000
target -= (57-ord("0"))*10000
target -= (6610-ord("0"))*1000
print(target)

print(alldigits)
