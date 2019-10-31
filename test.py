
# written by zhaoliyuan
# Fourier Analysis

import numpy as np
from scipy.fftpack import fft, ifft


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
        # 



if __name__ == '__main__':
    # linespace(start, end, frequency)
    # frequency should be no less than 2 times of signal's frequency
    x = np.linspace(0,1,10000)
    f1 = 500
    f2 = 500
    y = np.sin((2*np.pi)*x*f1) + 2*np.cos((2*np.pi)*x*f2)
    defaultSignal = y
    fourier = fourier(defaultSignal)
    fourier.fastFourier()
