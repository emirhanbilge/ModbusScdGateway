from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

from modbusManage import mdbs



def rangePeak(arr, freqIncreaseNumber, startFreq, FinishFreq):
    startingN = int(float(startFreq) / freqIncreaseNumber)
    print(" İstenen freqansın başlangıcı şu indexte : ", startingN)
    finishingN = int(float(FinishFreq) / freqIncreaseNumber)
    print("Bitme ındexi : ", finishingN)
    subArr = arr[startingN: finishingN]
    ind = np.argmax(subArr)
    print("Peak : ", subArr[ind])
    return startingN+ind



def getAnlaysis(refOverlap , reference):
    t, x = np.genfromtxt("XVerileri.csv", delimiter=',', unpack=True)


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

    valA = rangePeak(yEkseni, freqIncreaseNumber, 25, 38)  # dinamik olarak o ranch aralığında mı değil mi kontrol ettiğim yer
    v1 = 2.0/N * np.abs(yf[0:N//2])

    # Find peaks
    import peakutils
    peaks_ind1 = peakutils.indexes(v1, thres=0.05, min_dist=1)


    x = plt.subplots()
    plt.plot(xf, v1, color='black')


    peakArr = []
    for p in peaks_ind1:
        peakArr.append(p)
        ax.scatter(xf[p], v1[p], s=30, marker='s', color='red', label='v1')

    plt.xlabel('Freq (Hz)',fontsize=16,weight='bold')
    plt.ylabel('|Y(freq)|',fontsize=16,weight='bold')
    ax = plt.gca()
    plt.grid(True)
    plt.show()

    return [1 , 0,0]