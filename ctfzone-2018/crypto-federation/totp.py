import socket
import sys
import hmac
from struct import pack, unpack
from hashlib import sha1

host = 'crypto-04.v7frkwrfyhsjtbpfcppnu.ctfz.one'
port = 7331

totp_secret = "0b25610980900cffe65bfa11c41512e28b0c96881a939a2d"

sock = socket.create_connection((host, port))
sock.send(b"login </msg>")
time_on_server = sock.recv(1024)[:-6]
time_on_server = int(time_on_server)

counter = pack('>Q', int(time_on_server // 30))
totp_hmac = hmac.new(totp_secret.encode('UTF-8'), counter, sha1).digest()
offset = totp_hmac[19] & 15
totp_pin = str((unpack('>I', totp_hmac[offset:offset + 4])[0] & 0x7fffffff) % 1000000)

pin = totp_pin.zfill(6)
print(time_on_server)
print(pin)

sock = socket.create_connection((host, port))
sock.send(b"admin %s</msg>" % pin.encode("ascii"))
print(repr(sock.recv(1024)))
