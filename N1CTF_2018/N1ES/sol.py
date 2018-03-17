import base64, N1ES

round_keys = []
round_keys.append(['~', 'w', 'Y', 'k', 'k', '\x02', '\x05', '\x05'])
round_keys.append(['w', 'd', '}', '\x14', '?', '\x13', '\x04', 'W'])
round_keys.append(['l', '6', '\x08', '\x04', '\x13', '3', '\x19', '\x10'])
round_keys.append(['\x08', 'P', '2', '\x02', '/', 'W', '/', 'W'])
round_keys.append(['\x08', '\x14', '?', '@', 'W', '^', ' ', 'k'])
round_keys.append(['\x1b', '6', '^', '(', 'M', 'Y', '\x19', '\x02'])
round_keys.append(['3', 'f', 'w', '(', '\x13', '}', '\x08', 'u'])
round_keys.append(['=', '_', '\x13', 'M', '2', '=', '@', '\x04'])
round_keys.append(['z', '_', '~', '\x08', 'L', 'f', '\x19', 'z'])
round_keys.append(['I', 'Y', '\x01', '}', '/', '}', 'L', 'o'])
round_keys.append(['\x19', '\x05', '3', '\x01', 'z', 'w', '~', '?'])
round_keys.append(['L', 'B', '~', '\x13', '@', '6', '@', '\x05'])
round_keys.append(['\x08', 'd', '\x13', 'L', '^', '?', 'L', 'u'])
round_keys.append(['\x05', '{', 'M', 'P', 'M', '\n', 'z', 'P'])
round_keys.append(['k', '~', 'k', '/', 'o', 'u', '\x19', '\x04'])
round_keys.append(['o', 'k', '(', '\x13', 'I', 'f', ' ', '='])
round_keys.append(['~', '\x04', '\x08', '^', '\x02', '\n', '6', '3'])
round_keys.append(['/', '\x05', 'w', '2', ' ', 'd', '\x13', '6'])
round_keys.append([' ', '/', '}', '?', '\x04', '}', 'z', '\x19'])
round_keys.append(['\x05', '\n', '\n', 'l', '\x02', 'l', '^', 'l'])
round_keys.append(['k', '3', '}', '\x19', 'u', 'I', ' ', '^'])
round_keys.append(['~', 'B', '\x02', '}', 'k', '\x05', '\x02', '/'])
round_keys.append(['\n', '\x05', '^', '^', 'P', '}', '!', '{'])
round_keys.append(['\x08', 'W', 'u', 'o', ' ', '2', 'd', '\x04'])
round_keys.append(['/', 'W', 'w', '\x08', 'z', '\x19', '@', 'I'])
round_keys.append(['\x14', ' ', 'P', '!', '6', '6', ' ', '}'])
round_keys.append(['(', '!', '\x01', '\x08', 'd', '\x08', 'w', '?'])
round_keys.append(['u', 'W', '@', '\x13', '}', '~', '6', 'o'])
round_keys.append(['3', 'B', 'd', '\x01', 'W', '2', '\n', '6'])
round_keys.append(['}', '\x08', '6', '\x19', '&', '\x04', 'k', 'u'])
round_keys.append(['\x13', '2', '2', '(', '\x19', '{', '/', 'w'])
round_keys.append(['\x02', 'Y', ' ', 'W', '\x08', 'u', '\x01', 'I'])

encrypted_flag = base64.b64decode("HRlgC2ReHW1/WRk2DikfNBo1dl1XZBJrRR9qECMNOjNHDktBJSxcI1hZIz07YjVx")

def decrypt_single(x, key):
    sols = []
    for sol in range(256):
        if N1ES.round_add(chr(sol), key) == x:
            sols.append(sol)
    if len(sols) == 1:
        return chr(sols[0])
    else:
        print sols
        assert False

def decrypt_single_round(block, round_key):
    # a block here is 8 bytes
    sol = ""
    for i in range(8):
        sol += decrypt_single(block[i], round_key[i])
    return sol

def decrypt_whole_round(block, round_keys):
    round_outputs = [0] * 34
    round_outputs[33] = block[:8]
    round_outputs[32] = block[8:16]
    for i in xrange(31, -1, -1):
        round_outputs[i] = decrypt_single_round(round_outputs[i+2], round_keys[i])
    return round_outputs[0] + round_outputs[1]

print repr(encrypted_flag[32:40])
print repr(encrypted_flag[40:48])
print round_keys[-1]

soln = ""
for i in xrange(0, len(encrypted_flag), 16):
    soln += decrypt_whole_round(encrypted_flag[i:i+16], round_keys)
print soln
