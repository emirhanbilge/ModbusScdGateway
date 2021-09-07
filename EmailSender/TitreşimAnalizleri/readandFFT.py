from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal
import tkinter as tk
from tkinter import filedialog
import time


def rangePeak(arr, freqIncreaseNumber, startFreq, FinishFreq):
    startingN = int(float(startFreq) / freqIncreaseNumber)
    print(" İstenen freqansın başlangıcı şu indexte : ", startingN)
    finishingN = int(float(FinishFreq) / freqIncreaseNumber)
    print("Bitme ındexi : ", finishingN)
    subArr = arr[startingN: finishingN]
    ind = np.argmax(subArr)
    print("Peak : ", subArr[ind])
    return startingN+ind


# Prompt user for file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Two Column CSV", "*.csv")])
print(file_path)

# Load Data (assumes two column array
tic = time.time()
t, x = np.genfromtxt(file_path, delimiter=',', unpack=True)


# Number of sample points
N = len(x)  # Toplam kaç örneğimizin olduğu
# sample spacing
T = 1.0 / 400.0  # Periyodu burada biz 400 Hz örneklem aldığımız için 400'e bölüyorum

# 0 dan başlayarak toplam kaç saniye sürdüyse x eksenine onu yerleştirecek
x_axis = np.linspace(0.0, N*T, N, endpoint=False)
yf = fft(x)  # fftye y değerlerini yani accelerometre değerlerini gönderiyorum
xf = fftfreq(N, T)[:N//2]
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))


ax = plt.gca()  # get axis handle
line = ax.lines[0]  # get the first line, there might be more
te = line.get_xydata()
maxFreq = int(round(te[len(te)-1][0], 0))

TotalNumberofElement = len(te)
freqIncreaseNumber = float(maxFreq) / float(TotalNumberofElement)
print(" Freqans Artım oranı ", freqIncreaseNumber)
print(" Max Freq Lenght : ", maxFreq)

xEkseni = []
yEkseni = []

for i in te:
    yEkseni.append(i[1])
    xEkseni.append(i[0])
    #print("X : "  , i[0] , " Y:" , i[1])

valA = rangePeak(yEkseni, freqIncreaseNumber, 25, 38)


print("Peak Yapan Frekans : ", xEkseni[valA],
      "Peak Yaptığı değer : ", yEkseni[valA])

#print("Max : " , yEkseni[-3])
plt.show()
plt.grid()

