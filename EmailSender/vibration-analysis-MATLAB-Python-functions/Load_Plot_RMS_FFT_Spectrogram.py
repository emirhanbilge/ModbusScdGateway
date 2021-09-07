import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal
import tkinter as tk
from tkinter import filedialog
import time

#Prompt user for file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Two Column CSV","*.csv")])
print(file_path)

#Load Data (assumes two column array
tic = time.time()
t, x = np.genfromtxt(file_path,delimiter=',', unpack=True)


#Determine variables
N = np.int32(np.prod(t.shape))#length of the array , shape fonksiyonu arrayin uzunluğunu döndürür , prod da bu sayıyı kolay hesaplatmak içindir

Fs = 1/(t[1]-t[0]) 	#sample rate (Hz) Frekansı buldurdu
T = 1/Fs # periyodu buldurdu bu değişebileceğinden bu şekilde normalde t[1]-t[0] da aslında periyot
print("# Samples:",N)

#Plot Data
plt.figure(1)  
plt.plot(t, x)
plt.xlabel('Time (seconds)')
plt.ylabel('Accel (g)')
plt.title(file_path)
plt.grid()


#Compute RMS and Plot
tic = time.time()
w = np.int32(np.floor(Fs)); #width of the window for computing RMS
steps = np.int_(np.floor(N/w)); #Number of steps for RMS
t_RMS = np.zeros((steps,1)); #Create array for RMS time values
x_RMS = np.zeros((steps,1)); #Create array for RMS values
for i in range (0, steps):
	t_RMS[i] = np.mean(t[(i*w):((i+1)*w)])
	x_RMS[i] = np.sqrt(np.mean(x[(i*w):((i+1)*w)]**2));  
plt.figure(2)  
plt.plot(t_RMS, x_RMS)
plt.xlabel('Time (seconds)')
plt.ylabel('RMS Accel (g)')
plt.title('RMS - ' + file_path)
plt.grid()
toc = time.time()
print("RMS Time:",toc-tic)

#Compute and Plot FFT
tic = time.time()
plt.figure(3)  
xf = np.linspace(0.0, 0.5*T, N/2)
yf = fft(x)
plt.plot(xf, 2.0/N * np.abs(yf[0:np.int32(N/2)]))
plt.grid()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Accel (g)')
plt.title('FFT - ' + file_path)
toc = time.time()
print("FFT Time:",toc-tic)
"""
# Compute and Plot Spectrogram
tic = time.time()
plt.figure(4)  
f, t2, Sxx = signal.spectrogram(x, Fs, nperseg = Fs/4)
plt.pcolormesh(t2, f, np.log(Sxx))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram - ' + file_path)
toc = time.time()
print("Spectrogram Time:",toc-tic)
plt.show()
"""
