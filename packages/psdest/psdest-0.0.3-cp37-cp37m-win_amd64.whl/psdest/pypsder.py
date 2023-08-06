
import numpy as np
from scipy import signal



# https://gitlab.mpcdf.mpg.de/mtr/pocketfft

# from fftw tests
try:
    import mkl_fft
    # mkl_fft monkeypatches numpy.fft
    # explicitly import from fftpack or pocketfft instead
    try:
        # numpy 1.17 replaced fftpack with pocketfft
        from numpy.fft import pocketfft as np_fft
    except ImportError:
        from numpy.fft import fftpack as np_fft
except ImportError:
    from numpy import fft as np_fft



class PyPSDer(object):
    def __init__(self, Nft=None, rbw=None, rate=1., window='hann', step=0.5):
        self.rate = rate
        
        if Nft is None:
            self.Nft = int(rate / rbw)
        else:
            self.Nft = int(Nft)

        self.Nout = int(self.Nft // 2 + 1)
        self.Nstep = int(self.Nft * step)
        
        if window == 'box':
            self.window = 1
        else: 
            self.window = signal.get_window(window, self.Nft)
            self.window = self.window / np.mean(self.window)
            
        self.f = np.fft.rfftfreq(self.Nft, 1./rate)



    def psd(self, x):
        # if x is imaginary - double sided PSD
        # if x is real - single sided PSD
        # only single sided for now
        x = np.asarray(x)
        if np.iscomplexobj(x):
            raise RuntimeError("Complex (double-sided) PSDs not yet supported")
        XX = np.zeros(self.Nout)

        # recompute Navg incase length of s changes
        self.Navg = int((len(x) - self.Nft) / self.Nstep) + 1
        norm = 2. / float(self.Navg * self.Nft * self.rate)

        for i in range(self.Navg):
            inn = x[i * self.Nstep:i * self.Nstep + self.Nft] * self.window

            X = np.fft.rfft(inn)

            XX += (X.real**2 + X.imag**2) * norm

        XX[0] *= 0.5
        
        return XX

            
    def cross(self, x, y):
        x = np.asarray(x)
        y = np.asarray(y)

        N = len(x)
        if len(y) != N:
            raise RuntimeError(f"input arrays have to be same dimensions ({len(x)}, {len(y)})")

        if np.iscomplexobj(x) or np.iscomplexobj(y):
            raise RuntimeError("Only supports real x, y")

        XX = np.zeros(self.Nout)
        YY = np.zeros(self.Nout)
        XY = np.zeros(self.Nout, dtype=complex)

        # recompute Navg incase length of s changes
        self.Navg = int((N - self.Nft) / self.Nstep) + 1
        norm = 2. / float(self.Navg * self.Nft * self.rate)

        for i in range(self.Navg):
            inx = x[i * self.Nstep:i * self.Nstep + self.Nft] * self.window
            iny = y[i * self.Nstep:i * self.Nstep + self.Nft] * self.window

            X = np.fft.rfft(inx)
            Y = np.fft.rfft(iny)

            XX += (X.real**2 + X.imag**2) * norm
            YY += (Y.real**2 + Y.imag**2) * norm
            XY += X * Y.conj() * norm

        XX[0] *= 0.5
        YY[0] *= 0.5
        XY[0] *= 0.5
        
        return XX, YY, XY