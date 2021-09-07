# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 11:43:49 2021

@author: EBB
"""

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


firstAnalysis = 300000
plt.figure(1)  
plt.plot(t[0:firstAnalysis], x[0: firstAnalysis])
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
xWc = int(N)%2
xW = 5000
if xWc :
    
    xW +=1

ebbC = 0
brc = 10000

meanCross = []

while(ebbC < 15):
    
    print("Brc : " , brc)
    xf = np.linspace(0.0, xW*T, xW  ,endpoint=False)  # başından sonuna kadar göster ve yay
    yf = fft(x[0+brc: 10000+brc])         #değerler için fft uygula 
    c = np.fft.rfft(x[0+brc: 10000+brc])
    print(len(c))
    fig = plt.plot(xf, 2.0/xW * np.abs(c[0:10000]))     #Oturt
    #plt.grid()
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Accel (g)')
    plt.title('FFT - ' + file_path)
    ax = plt.gca() # get axis handle
    line = ax.lines[0] # get the first line, there might be more
    te =  line.get_xydata()
    brc += 10000
    summMean = 0
    counter = 0
    for i in te:
        if round(i[0],4) ==  0.04 : 
            summMean += i[1]
            counter += 1
           #♦ print("Max :  " , i[0] ,"  Val : " , i[1])
    try:
        summMean = summMean / counter
    except:
        sumMean = 0
    if len(meanCross) == 0:
        print("Ortalama 1.2 hz deki amplitutesi : " , summMean)
        meanCross.append(summMean)
    else:
        if (meanCross[0]-meanCross[0]*0.2 < summMean or summMean> meanCross[0]*0.2+meanCross[0])  and summMean!=meanCross[0]   :
            print(meanCross[0] , " ********** summMean : " , summMean )
            print("Alarm Balansızlık Tespit Edildi")
        else:
            print("Balanslı")
    ebbC +=1
