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
print("Veri uzunluğu " , N)
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
w = np.int32(np.floor(Fs)); #width of the window for computing RMS , burada array içerisindeki en yüksek değer geldi galiba en düşük


steps = np.int_(np.floor(N/w)); #Number of steps for RMS toplamda grafiği kaç parçaya böleceğini hesapladı step buna eşit
t_RMS = np.zeros((steps,1)); #Create array for RMS time values zamanları bu hesaplanan parça uzunluğuna göre böldü
x_RMS = np.zeros((steps,1)); #Create array for RMS values değerleri bu hesaplanan parça uzunluğuna göre böldü
for i in range (0, steps):
	t_RMS[i] = np.mean(t[(i*w):((i+1)*w)])   # burada o hesap için gerekli ölçümlemeleri yaptı bunların formülasyonları var
	x_RMS[i] = np.sqrt(np.mean(x[(i*w):((i+1)*w)]**2));   # burada da aynı şekilde hesaplamalar yapılıyor
plt.figure(2)  
plt.plot(t_RMS, x_RMS)
plt.xlabel('Time (seconds)')
plt.ylabel('RMS Accel (g)')
plt.title('RMS - ' + file_path)
plt.grid()




#Compute and Plot RFFT 
N = len(t)     #Manuel uzunluğu girmemiz lazım shape çünkü bir tupple döndürmekte
plt.figure()  
xf = np.linspace(0.0, N*T, 150007,endpoint=False)  # başından sonuna kadar göster ve yay
yf = fft(x)         #değerler için fft uygula 

c = np.fft.rfft(x)
print(len(c))
fig = plt.plot(xf, 2.0/N * np.abs(c[0:N]))     #Oturt
#plt.grid()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Accel (g)')
plt.title('FFT - ' + file_path)
ax = plt.gca() # get axis handle


fig.savefig('outP.svg', format='svg')
line = ax.lines[0] # get the first line, there might be more

te =  line.get_xydata()
for i in te:
    if i[1] > 5:
        print(i)

N = len(t)     #Manuel uzunluğu girmemiz lazım shape çünkü bir tupple döndürmekte
plt.figure()  
xf = np.linspace(0.0, N*T, N,endpoint=False)  # başından sonuna kadar göster ve yay
yf = fft(x)         #değerler için fft uygula 

    
"""
plt.plot(xf, 2.0/N * np.abs(yf[0:N]))     #Oturt
plt.grid()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Accel (g)')
plt.title('FFT - ' + file_path)
# import required modules

  
signal = np.array(x, dtype=float)
fourier =np.fft.rfft(signal)
print(fourier)
n = signal.size
timestep = 0.01
freq = np.fft.fftfreq(n, d=timestep)


"""
"""
xf = np.linspace(0.0, N*T, 600000,endpoint=False)
plt.plot(t, freq)
a = (freq.sort())
print(freq[-1000])
"""


"""

# compute frequency associated
# with coefficients
freqs = np.fft.fftfreq(len(x))

# extract frequencies associated with FFT values
for coef, freq in zip(w, freqs):
    if coef:
        print('{c:>6} * exp(2 pi i t * {f})'.format(c=coef,
                                                    f=freq))

"""

# Compute and Plot Spectrogram
"""
plt.figure(4)  
f, t2, Sxx = signal.spectrogram(x, Fs)

plt.pcolormesh(t2, f, np.log(Sxx))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram - ' + file_path)
plt.show()
"""
