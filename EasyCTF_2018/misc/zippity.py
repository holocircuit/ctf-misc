import socket
import sys
import re

def load_data(f):
    l = open(f, "rb").readlines()[1:]
    l = [s.strip().split(b",") for s in l]

    lat_dict = {m[0] : m[1].strip() for m in l}
    long_dict = {m[0] : m[2].strip() for m in l}
    return (lat_dict, long_dict)

def load_census_data(f):
    l = open(f, "rb").readlines()
    title = l[0].strip().split(b",")
    rows = [s.strip().split(b",") for s in l[1:]]

    # the service expects padded zipcodes
    # sadly, it looks like some codes appear in multiple rows - I'm not sure why
    rows_dict = {row[0].zfill(5) : row for row in rows }
    title = { col : i for (i, col) in enumerate(title) }
    return (title, rows_dict)

# from some Github page
(lat_dict, long_dict) = load_data("zipcode.data")

# from the Census website, weirdly didn't include lat/long
(census_title, census_dict) = load_census_data("waterdata.csv")

print("Connecting...")
TCP_IP = 'c1.easyctf.com'
TCP_PORT = 12483

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))

for i in range(50):
    msg = s.recv(1024)
    print(repr(msg))
    zip_code = re.findall(b"zip code ([0-9]*)", msg)
    if zip_code == []:
        print("No zip code found :(")
        assert False
    zip_code = zip_code[0]
    print("[+] ZIP code: %s" % zip_code)
  
    if b"longitude" in msg:
        resp = long_dict[zip_code]
        print("[+] Recognised as longitude, sending response %s" % resp)
        s.send(resp + b"\n")
    elif b"latitude" in msg:
        resp = lat_dict[zip_code]
        print("[+] Recognised as latitude, sending response %s" % resp)
        s.send(resp + b"\n")
    elif b"water area" in msg:
        census_row = census_dict[zip_code]
        area_col = census_title[b"AREAPT"]
        land_area_col = census_title[b"AREALANDPT"]
        area = int(census_row[area_col])
        land_area = int(census_row[land_area_col])
        water_area = area - land_area
        print("[+] Area = %d, land area = %d, calculated water area = %d" % (area, land_area, water_area))
        resp = str(water_area).encode("ascii")
        s.send(resp + b"\n")
    elif b"land area" in msg:
        census_row = census_dict[zip_code]
        land_area_col = census_title[b"AREALANDPT"]
        resp = census_row[land_area_col]
        print("[+] Recognised as land area, sending %s" % resp)
        s.send(resp + b"\n")
    else:
        print("Failed to recognise :(")
        s.send(b"nonsense\n")
        print(s.recv(1024))
        assert False
