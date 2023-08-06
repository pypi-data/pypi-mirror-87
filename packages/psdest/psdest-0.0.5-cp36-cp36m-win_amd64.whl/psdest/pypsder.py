
import numpy as np
from scipy import signal



# https://gitlab.mpcdf.mpg.de/mtr/pocketfft

# from fftw tests
try:
    import mkl_fft
except:
    pass
#     # mkl_fft monkeypatches numpy.fft
#     # explicitly import from fftpack or pocketfft instead
#     try:
#         # numpy 1.17 replaced fftpack with pocketfft
#         from numpy.fft import pocketfft as np_fft
#     except ImportError:
#         from numpy.fft import fftpack as np_fft
# except ImportError:
#     from numpy import fft as np_fft



class PyPSDer(object):
    def __init__(self, Nft=None, rbw=None, rate=1., window='hann', step=0.5, threads=1, dtype=np.float64):
        self.rate = rate
        
        if Nft is None:
            self.Nft = int(rate / rbw)
        else:
            self.Nft = int(Nft)

        if np.dtype(dtype).char in np.typecodes['Complex']:
            self.is_complex = True
            self.Nout = int(self.Nft)
            self._fft = np.fft.fft
        else:
            self.is_complex = False
            self.Nout = int(self.Nft // 2 + 1)
            self._fft = np.fft.rfft
        self.Nstep = int(self.Nft * step)
        
        if window == 'box':
            self.window = 1
        else: 
            self.window = signal.get_window(window, self.Nft)
            self.window = self.window / np.mean(self.window)
            

    @property
    def f(self):
        if self.is_complex:
            return np.fft.fftfreq(self.Nft, 1. / self.rate)
        else:
            return np.fft.rfftfreq(self.Nft, 1. / self.rate)


    def psd(self, x):
        x = np.asarray(x)
        if np.iscomplexobj(x) and self.is_complex == False:
            raise RuntimeError("PSDer set up for real transforms, but array complex")
        
        
        XX = np.zeros(self.Nout)

        # recompute Navg incase length of s changes
        self.Navg = int((len(x) - self.Nft) / self.Nstep) + 1


        norm = 1. / float(self.Navg * self.Nft * self.rate)
        if not self.is_complex:
            # single-sided psd
            norm *= 2.

        for i in range(self.Navg):
            inn = x[i * self.Nstep:i * self.Nstep + self.Nft] * self.window

            X = self._fft(inn)

            XX += (X.real**2 + X.imag**2) * norm

        if not self.is_complex: 
            # single-sided psd
            XX[0] *= 0.5
        
        return XX

            
    def cross(self, x, y):
        x = np.asarray(x)
        y = np.asarray(y)

        N = len(x)
        if len(y) != N:
            raise RuntimeError(f"input arrays have to be same dimensions ({len(x)}, {len(y)})")

        if np.iscomplexobj(x) or np.iscomplexobj(y):
            if self.is_complex == False:
                raise RuntimeError("PSDer set up for real transforms, but array complex")

        XX = np.zeros(self.Nout)
        YY = np.zeros(self.Nout)
        XY = np.zeros(self.Nout, dtype=complex)

        # recompute Navg incase length of s changes
        self.Navg = int((N - self.Nft) / self.Nstep) + 1
        norm = 1. / float(self.Navg * self.Nft * self.rate)
        if not self.is_complex:
            # single-sided psd
            norm *= 2.

        for i in range(self.Navg):
            inx = x[i * self.Nstep:i * self.Nstep + self.Nft] * self.window
            iny = y[i * self.Nstep:i * self.Nstep + self.Nft] * self.window

            X = self._fft(inx)
            Y = self._fft(iny)

            XX += (X.real**2 + X.imag**2) * norm
            YY += (Y.real**2 + Y.imag**2) * norm
            XY += X * Y.conj() * norm

        if not self.is_complex:
            XX[0] *= 0.5
            YY[0] *= 0.5
            XY[0] *= 0.5
        
        return XX, YY, XY
