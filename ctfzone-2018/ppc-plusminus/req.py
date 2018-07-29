import socket

sock = socket.create_connection(("ppc-01.v7frkwrfyhsjtbpfcppnu.ctfz.one", 2445))

def do_op(number1, number2, op):
    if op == "+":
        return number1+number2
    if op == "*":
        return number1*number2
    if op == "-":
        return number1-number2
    if op == "/":
        if number2 == 0:
            return None
        else:
            return number1/number2

def make_instructions(numbers, target):
    # Just going to brute-force until we reach the target
    # a set of instructions will be a list of (idx, operation)
    # which means "put brackets around idx, idx + 1 and apply the operation"

    # base case
    if len(numbers) > 5:
       print("Calling make_instructions with %d" % len(numbers))
    if len(numbers) == 1:
        if numbers[0] == target:
            yield []
        return

    for idx in range(len(numbers) - 1):
        for operation in "+-*/":
            instruction = (idx, operation)
            new_number = do_op(numbers[idx], numbers[idx+1], operation)
            if new_number != None:
                numbers2 = numbers[:idx] + [new_number] + numbers[idx+2:]
                for instructions in make_instructions(numbers2, target):
                    yield [instruction] + instructions

# assumes numbers are strings
def make_string(numbers, instructions):
    for (idx, op) in instructions:
        numbers = numbers[:idx] + ["(%s%s%s)" % (numbers[idx], op, numbers[idx+1])] + numbers[idx+2:]
    return "".join(numbers)

numbers = [7, 3, 38, 66, 38, 9, 51, 18]
target = -4.998522895125554

def read_line(sock):
    l = []
    while True:
        l.append(sock.recv(1))
        if l[-1] == b"\n":
            break

    return b"".join(l)

while True:
    s = read_line(sock)
    print("Line from server:", s)
    numbers = s.strip().split(b" ")
    target = numbers[-1]
    numbers = [n.decode("ascii") for n in numbers[:-1]]

    print(numbers)
    numbers_n = list(map(float, numbers))
    instructions = make_instructions(numbers_n, float(target)).__next__()

    response = make_string(numbers, instructions)
    print(response)

    sock.send(response.encode("ascii"))
    sock.send(b"\n")
    s = read_line(sock)

    print("Response from server:", s)
