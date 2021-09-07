# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 14:03:15 2021

@author: EBB
"""""
"""
import numpy as np
from matplotlib import pyplot as plt

SAMPLE_RATE = 5000  # Hertz
DURATION = 60  # Seconds

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

# Generate a 2 hertz sine wave that lasts for 5 seconds
x, y = generate_sine_wave(2, SAMPLE_RATE, DURATION)
plt.plot(x, y)
plt.show()


"""


from scipy.fft import  fftfreq
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal
import tkinter as tk
from tkinter import filedialog
import time

# Prompt user for file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Two Column CSV", "*.csv")])
print(file_path)

# Load Data (assumes two column array
tic = time.time()
t, x = np.genfromtxt(file_path, delimiter=',', unpack=True)

"""
print(t)
print(x)
"""

# Number of sample points
N = len(x)  # Toplam kaç örneğimizin olduğu
# sample spacing
T = 1.0 / 400.0  # Periyodu burada biz 400 Hz örneklem aldığımız için 400'e bölüyorum

# 0 dan başlayarak toplam kaç saniye sürdüyse x eksenine onu yerleştirecek
x_axis = np.linspace(0.0, N*T, N, endpoint=False)


yf = fft(x)  # fftye y değerlerini yani accelerometre değerlerini gönderiyorum

print(yf)



xf = fftfreq(N, T)[:N//2]

plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))

plt.show()

"""

import matplotlib.pyplot as plt
plt.plot(t[0:firstAnalysis], x[0: firstAnalysis])
plt.xlabel('Time (seconds)')
plt.ylabel('Accel (g)')
plt.title(file_path)
plt.grid()"""
