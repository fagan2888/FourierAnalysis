
# written by zhaoliyuan
# Fourier Analysis

import numpy as np
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt


class fourier:

    def __init__(self, defaultSignal):
        self.signal = defaultSignal

    def fastFourier (self):
        signal = self.signal
        # fast fourier analysis
        out = fft(signal)
        # get real part
        outReal = out.real
        # get imaginary part
        outImag = out.imag
        
        # get alll energy and frequency of different signals
        yf = abs(out)
        xf = np.arange(len(y))
        
        yf1 = yf[range(len(x)//2)]
        xf1 = xf[range(len(x)//2)]
        
        # plot
        plt.subplot(131)
        plt.plot(x[0:50],y[0:50])
        plt.title('original signal')
        
#        plt.subplot(132)
#        plt.plot(xf,yf)
#        plt.title('original signal fast fourier transferred')

        plt.subplot(133)
        plt.plot(xf1,yf1)
        plt.title('original signal fast fourier transferred')

        plt.show()


if __name__ == '__main__':
    # linespace(start, end, frequency)
    # frequency should be no less than 2 times of signal's frequency
    x = np.linspace(0,1,20000)
    f1 = 500
    f2 = 5000
    y = np.sin((2*np.pi)*x*f1) + 2*np.cos((2*np.pi)*x*f2)
    defaultSignal = y
    fourier = fourier(defaultSignal)
    fourier.fastFourier()
