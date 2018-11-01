import struct
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

s = open("audio.wav","rb").read()
wFormatTag, nChannels, sampleRate, byteRate, blockAlign, bitsPerSample = struct.unpack("<HHIIHH", s[20:36])

print wFormatTag
print nChannels
print sampleRate
print byteRate
print blockAlign
print bitsPerSample

bytesPerSample = bitsPerSample / 8

samples = [struct.unpack("d", s[i:i+8])[0] for i in xrange(44, len(s), 8)]

"""
x1 = np.array(samples)
Fs = sampleRate
plt.specgram(x1, NFFT=2048, Fs=Fs)  
plt.title("x1")  
plt.ylim(-Fs/2, Fs/2)  
plt.savefig("x1_spec.pdf", bbox_inches='tight', pad_inches=0.5)  
plt.close()
"""

def scatter_plot(x, color):
  plt.scatter(np.real(x), np.imag(x), c=color)

Fs = sampleRate

x = np.array(samples)
y = signal.hilbert(x)

def try_and_get_signal(complex_audio, carrier_frequency_guess):
  # remove carrier frequency. 
  fc = np.exp(-1.0j*2.0*np.pi* carrier_frequency_guess/Fs*np.arange(len(y)))
  z = y * fc

  # multiply by conjugate of next, to get phase difference
  phase_difference = z[:-1] * np.conj(z[1:])
  signal = np.angle(phase_difference)

  return signal

def phase_shift(signal, freq):
  fc = np.exp(-1.0j*2.0*np.pi* freq/Fs*np.arange(len(signal)))
  return signal * fc

y = phase_shift(y, 106000)
y_diff = y[1:] * np.conj(y[:-1])
phase = np.angle(y_diff)

plt.plot(phase)
plt.show()

wav = ""
for p in phase:
  int_level = int(p * 0x10000 / (2.0 * np.pi))
  print p, int_level
  wav += struct.pack("<h", int_level)

import wave
w = wave.open("test.wav","wb")
w.setparams((1, 2, 44000, 0, "NONE", "NONE"))
w.writeframes(wav)
w.close()
