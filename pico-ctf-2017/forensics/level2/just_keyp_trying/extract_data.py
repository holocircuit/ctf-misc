from scapy.all import *

packets = rdpcap("data.pcap")
data = [raw(packet)[-8:] for packet in packets]

def shift(key):
  if key != key.upper():
    return key.upper()

  
  if key == "[": return "{"
  if key == "]": return "}"
  if key == "-": return "_"
  if key == "\x00": return None
  
  print "Don't know how to convert %s to shift" % key
  assert False

def parse_single_data(data):
  modifier = ord(data[0])
  key = ord(data[2])

  mapping = "\x00***abcdefghijklmnopqrstuvwxyz1234567890***\t -=[]"
  key = mapping[key]

  if data == "\x00\x00\x00\x00\x00\x00\x00\x00": return None

  if modifier == 0:
    return key
  if modifier == 32: # left shift
    return shift(key)
  if modifier == 1: # left control
    if key == "\x00": 
      return None
    if key == "c": 
      return None
    print "unknown key with left control: %s" % key
    print repr(data)
    assert False
  print "unknown modifier: %d" % modifier
  assert False

parsed_data = map(parse_single_data, data)
parsed_data = filter(lambda d: d is not None, parsed_data)

print "".join(parsed_data)
