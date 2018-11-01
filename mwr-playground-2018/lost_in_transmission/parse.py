import struct
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

s = open("lost-in-transmission.wav","rb").read()
wFormatTag, nChannels, sampleRate, byteRate, blockAlign, bitsPerSample = struct.unpack("<HHIIHH", s[20:36])

print "wFormatTag", wFormatTag
print "nChannels", nChannels
print "sampleRate", sampleRate
print "byteRate", byteRate
print "blockAlign", blockAlign
print "bitsPerSample", bitsPerSample

# Abusing terminology here: "sample" = a pair of samples, for each side
samples = [struct.unpack("<hh", s[i:i+4]) for i in xrange(44, len(s), 4)]

print len(samples)
start1 = 3480000
start2 = 3500000

def plot(start, end, color):
  x = np.array(map(lambda l : l[0], samples[start:end]))
  y = np.array(map(lambda l : l[0] - l[1], samples[start:end]))
  plt.scatter(x, y, c=color)

plot(start1, start2, "c")
#plot(start2, start3, "r")

plt.show()
