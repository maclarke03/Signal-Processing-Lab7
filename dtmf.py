# Micah Clarke
# ID: 1001288866

from scipy.signal import freqz
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram


def processTones(name, L, fs, samplesPerTone) :

    def freqResponseFilters(signal,fs,f1209,f1336,f1477,f697,f770,f852,f941):
        
        
        x,y = freqz(f1209,1)
        x1,y1 = freqz(f1336,1)
        x2,y2 = freqz(f1477,1)
        x3,y3 = freqz(f697,1)
        x4,y4 = freqz(f770,1)
        x5,y5 = freqz(f852,1)
        x6,y6 = freqz(f941,1)
        
        plt.figure()
        f = fs * x / (2 * np.pi)
        plt.plot(f,abs(y))
        f = fs * x1 / (2 * np.pi)
        plt.plot(f,abs(y1))
        f = fs * x2 / (2 * np.pi)
        plt.plot(f,abs(y2))
        f = fs * x3 / (2 * np.pi)
        plt.plot(f,abs(y3))
        f = fs * x4 / (2 * np.pi)
        plt.plot(f,abs(y4))
        f = fs * x5 / (2 * np.pi)
        plt.plot(f,abs(y5))
        f = fs * x6 / (2 * np.pi)
        plt.plot(f,abs(y6))

        plt.title("Frequency Responses of Bandpass Filters")
        plt.xlabel("Hertz")
        plt.show()

        f,t,Sxx = spectrogram(signal,fs)
        plt.pcolormesh(t,f,Sxx)
        plt.ylabel("Frequency [Hz]")
        plt.xlabel("Time [sec]")
        plt.show()
        


    def bandPassFilter(signal,L,fs,f1209,f1336,f1477,f697,f770,f852,f941):
        # Filter bank for touchpad, added the two frequencies that makeup the touchpad value and used them as keys to the values
        bank = {
            1906: ("1"),
            2033: ("2"),
            2174: ("3"),
            1979: ("4"),
            2106: ("5"),
            2247: ("6"),
            2061: ("7"),
            2188: ("8"),
            2329: ("9"),
            2150: ("*"),
            2277: ("0"),
            2418: ("#")
            }
        # Lookup frequency based off indexes from 1st and 2nd highest mean values from array
        freqBank = {
            0: "1209",
            1: "1336",
            2: "1477",
            3: "697",
            4: "770",
            5: "852",
            6: "941"
            }
        
        meanValues = []
        
        meanValues.append(np.mean(np.convolve(signal,f1209)**2))
        meanValues.append(np.mean(np.convolve(signal,f1336)**2))
        meanValues.append(np.mean(np.convolve(signal,f1477)**2))
        meanValues.append(np.mean(np.convolve(signal,f697)**2))
        meanValues.append(np.mean(np.convolve(signal,f770)**2))
        meanValues.append(np.mean(np.convolve(signal,f852)**2))
        meanValues.append(np.mean(np.convolve(signal,f941)**2))

        # Finds the 1st and 2nd highest values from array, keeps track of indexes 
        firstIndex = secondIndex = 0
        first = second = -10000
        for i in range(0,len(meanValues)):
            if(meanValues[i] > first):
               second = first
               secondIndex = firstIndex
               first = meanValues[i]
               firstIndex = i
            elif(meanValues[i] > second and meanValues[i] < first):
               second = meanValues[i]
               secondIndex = i
        # Get value from key and adds the two frequencies found
        firFreq = freqBank.get(firstIndex)
        secFreq = freqBank.get(secondIndex)
        total = int(firFreq)+int(secFreq)
       
        # Get the touchpad value from the addition of the two frequencies found above
        value = bank.get(total)
        return value
    
        
    # Importing csv values 
    signal = np.genfromtxt(name, delimiter = ',')
    # Determing number of tones from the csv file
    numTones = len(signal) / samplesPerTone


    # Filter coefficients per frequency
    f1209 = []
    f1336 = []
    f1477 = []
    f697 = []
    f770 = []
    f852 = []
    f941 = []

    # Produces the filter coefficients just once for the program
    n = 0
    while n < L:
        f1209.append(((2 / L) * (np.cos((2 * np.pi * 1209 * n) / fs))))
        f1336.append(((2 / L) * (np.cos((2 * np.pi * 1336 * n) / fs))))
        f1477.append(((2 / L) * (np.cos((2 * np.pi * 1477 * n) / fs))))
        f697.append(((2 / L) * (np.cos((2 * np.pi * 697 * n) / fs))))
        f770.append(((2 / L) * (np.cos((2 * np.pi * 770 * n) / fs))))
        f852.append(((2 / L) * (np.cos((2 * np.pi * 852 * n) / fs))))
        f941.append(((2 / L) * (np.cos((2 * np.pi * 941 * n) / fs))))
        n += 1
    
    # Slices through the signal to obtain the value from each bin
    i = 0
    k = 0
    decode = []
    while i < numTones:
        decode.append(bandPassFilter(signal[k:4001+k],L,fs,f1209,f1336,f1477,f697,f770,f852,f941))
        i += 1
        k += 4000

   
    freqResponseFilters(signal,fs,f1209,f1336,f1477,f697,f770,f852,f941)
    
    # Removes the white spaces 
    answer = ''
    for element in decode:
        answer += element
        

    return answer

#############  main  #############
if __name__ == "__main__":
    filename = "tones-7481414.csv"  #  name of file to process
    L = 64                  #  filter length
    fs = 8000               #  sampling rate
    samplesPerTone = 4000   #  4000 samples per tone, 
                            #    NOT the total number of samples per signal

    # returns string of telephone buttons corresponding to tones
    phoneNumber = processTones(filename, L, fs, samplesPerTone)
    
    print(phoneNumber)
