from signals import SignalGenerator, SignalOperations
from filesRW import FileRW
import numpy as np
from plots import plot_raw_signal, plot_raw_points
from matplotlib import pyplot as plt
from plots import plot_W1, plot_W2


class Transfomations:
    @staticmethod
    def generate_signals():
        # ✅ 
        f_pr = 16  # Hz
        T = 1 / f_pr
        N = 64  # liczba próbek 
        t = np.arange(N) * T

        S1 = 2 * np.sin(2 * np.pi * (1/2) * t + np.pi/2) + 5 * np.sin(2 * np.pi * (1/0.5) * t + np.pi/2)
        S2 = 2 * np.sin(2 * np.pi * (1/2) * t) + np.sin(2 * np.pi * (1/1) * t) + 5 * np.sin(2 * np.pi * (1/0.5) * t)
        S3 = 5 * np.sin(2 * np.pi * (1/2) * t) + np.sin(2 * np.pi * (1/0.25) * t)

        return S1, S2, S3

    @staticmethod
    def dft(x):
        # ✅
        N = len(x)
        X = np.zeros(N, dtype=complex)
        for k in range(N):
            for n in range(N):
                X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
        return X
    
    @staticmethod
    def reverse_fourier(X):
        # ✅
        N = len(X)
        x = np.zeros(N, dtype=complex)
        for n in range(N):
            for k in range(N):
                x[n] += X[k] * np.exp(2j * np.pi * k * n / N)
        return x / N

    @staticmethod
    def fft_dit(x):
        # ✅
        N = len(x)
        if N <= 1:
            return x
        even = Transfomations.fft_dit(x[0::2])
        odd = Transfomations.fft_dit(x[1::2])
        T = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
        result = [even[k] + T[k] for k in range(N // 2)] + \
            [even[k] - T[k] for k in range(N // 2)]
        return np.array(result, dtype=complex) 

    @staticmethod
    def fft_dif(x):
        # ❌
        x = np.array(x, dtype=complex)
        N = len(x)
        stages = int(np.log2(N))
        for stage in range(stages):
            step = 2 ** (stage + 1)
            half_step = step // 2
            for k in range(0, N, step):
                for j in range(half_step):
                    u = x[k + j]
                    v = x[k + j + half_step] * np.exp(-2j * np.pi * j / step)
                    x[k + j] = u + v
                    x[k + j + half_step] = u - v
        # Bit-reversed order at the end
        j = 0
        for i in range(1, N):
            bit = N >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                x[i], x[j] = x[j], x[i]
        return x
    
    @staticmethod
    def dct(x):
        # ✅
        N = len(x)
        result = np.zeros(N)
        for m in range(N):
            cm = np.sqrt(1/N) if m == 0 else np.sqrt(2/N)
            sum_val = 0
            for n in range(N):
                sum_val += x[n] * np.cos(np.pi * (2*n + 1) * m / (2 * N))
            result[m] = cm * sum_val
        return result
    
    @staticmethod
    def reverse_dct(X):
        # ✅
        N = len(X)
        result = np.zeros(N)
        for n in range(N):
            sum_val = 0
            for m in range(N):
                cm = np.sqrt(1/N) if m == 0 else np.sqrt(2/N)
                sum_val += cm * X[m] * np.cos(np.pi * (2*n + 1) * m / (2 * N))
            result[n] = sum_val
        return result
    
    @staticmethod
    def fct(x):
        # ✅
        N = len(x)
        y = np.zeros(2*N)
        y[0:N] = x
        y[N:] = x[::-1]

        # TODO: 
        # Y = np.fft.fft(y)
        # Y = Transfomations.dft(y)
        Y = Transfomations.fft_dit(y)

        factor = np.exp(-1j * np.pi * np.arange(N) / (2 * N))
        X = np.real(Y[:N] * factor)

        return X
    
    @staticmethod
    def reverse_fct(X):
        # ✅
        N = len(X)
        x = np.zeros(N, dtype=complex)
        for n in range(N):
            for k in range(N):
                x[n] += X[k] * np.cos(np.pi * k * (n + 0.5) / N)
        return x / N

    @staticmethod
    def hadamard_matrix(N):
        if N == 1:
            return np.array([[1]])
        H = Transfomations.hadamard_matrix(N // 2)
        return np.block([[H, H], [H, -H]])
    
    @staticmethod
    def wht(x):
        N = len(x)
        assert (N & (N - 1)) == 0, "Długość sygnału musi być potęgą 2"

        H = Transfomations.hadamard_matrix(N)
        return H @ x
    
    @staticmethod
    def fwht(x):
        x = x.copy().astype(float)
        N = len(x)
        assert (N & (N - 1)) == 0, "Długość sygnału musi być potęgą 2"

        h = 1
        while h < N:
            for i in range(0, N, h * 2):
                for j in range(i, i + h):
                    a = x[j]
                    b = x[j + h]
                    x[j]     = a + b
                    x[j + h] = a - b
            h *= 2
        return x
    
    @staticmethod
    def reverse_fwht(x):
        N = len(x)
        return Transfomations.fwht(x) / N


def test_dft():
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    # plot_raw_signal(s1, t, toplot=True)
    # test()
    # TODO nwm jak to sprawdzić, czy działa
    from scipy.fft import fft
    npdft = fft(s2)  # NumPy DFT

    X_dft = Transfomations.dft(s2)
    x2 = Transfomations.reverse_fourier(X_dft)

    plot_raw_signal(s2, t, toplot=True)
    plot_raw_signal(npdft, t, toplot=True)
    plot_raw_signal(X_dft, t, toplot=True)
    plot_raw_signal(x2, t, toplot=True)

    plot_W1(npdft, title="NumPy")
    plot_W2(npdft, title="NumPy")
    plot_W1(X_dft, title="Sygnal", stem=True)
    plot_W2(X_dft, title="sygnal")

def test_fft():
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T

    npfft = np.fft.fft(s2)  # NumPy FFT
   
    X_fft_dit = Transfomations.fft_dit(s2)
    X_fft_dif = Transfomations.fft_dif(s2)
    
    # x2_dit = Transfomations.reverse_fft(X_fft_dit)
    # x2_dif = Transfomations.reverse_fft(X_fft_dif)
    x2_dit = Transfomations.reverse_fourier(X_fft_dit)
    x2_dif = Transfomations.reverse_fourier(X_fft_dif)
    plot_raw_signal(s2, t, toplot=True)
    plot_raw_signal(npfft, t, toplot=True)
    plot_raw_signal(X_fft_dit, t, toplot=True)
    plot_raw_signal(X_fft_dif, t, toplot=True)
    plot_raw_signal(x2_dit, t, toplot=True)
    plot_raw_signal(x2_dif, t, toplot=True)


    # plot_W1(X_fft_dit, title="FFT DIT")
    # plot_W2(X_fft_dit, title="FFT DIT - Amplituda")
    
    # plot_W1(X_fft_dif, title="FFT DIF")
    # plot_W2(X_fft_dif, title="FFT DIF - Amplituda")

def test_dct():
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    # ✅
    from scipy.fftpack import fft, dct
    npdct = dct(s3)  # DCT Type-II with orthonormal normalization
    X_dct = Transfomations.dct(s3)
    x2_dct = Transfomations.reverse_dct(X_dct)

    plot_raw_signal(s3, t, toplot=True)
    plot_raw_signal(npdct, t, toplot=True)
    plot_raw_signal(X_dct, t, toplot=True)
    plot_raw_signal(x2_dct, t, toplot=True)


def test_fct():
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    from scipy.fftpack import fft, dct
    npdct = dct(s1)  # DCT Type-II with orthonormal normalization
    X_fct = Transfomations.fct(s1)
    x2_fct = Transfomations.reverse_fct(X_fct)
    plot_raw_signal(s1, t, toplot=True)
    plot_raw_signal(npdct, t, toplot=True)
    plot_raw_signal(X_fct, t, toplot=True)
    plot_raw_signal(x2_fct, t, toplot=True)



def test_hadamard():
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T

    from scipy.linalg import hadamard
    nphadamard = hadamard(N) @ s1
    # ❌
    X_hadamard = Transfomations.wht(s1)
    x2_hadamard = Transfomations.reverse_fwht(X_hadamard)

    plot_raw_signal(s1, t, toplot=True)
    plot_raw_signal(nphadamard, t, toplot=True)
    plot_raw_signal(X_hadamard, t, toplot=True)
    plot_raw_signal(x2_hadamard, t, toplot=True)


def test_fast_hadamard():
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    # ❌
    X_fast_hadamard = Transfomations.fwht(s1)
    x2_fast_hadamard = Transfomations.reverse_fwht(X_fast_hadamard)
    plot_raw_signal(s1, t, toplot=True)
    plot_raw_signal(X_fast_hadamard, t, toplot=True)
    plot_raw_signal(x2_fast_hadamard, t, toplot=True)


if __name__ == "__main__":
    '''
    zwykła i szybka i jakiś wariant nwm
    transformacja cosinusowa i szybka
    i hadamarda i szybką?
    przekształcenia falkowego nie trzeba
    # '''
    # test_dft()
    test_fft()
    # test_dct()
    # test_fct()
    # test_hadamard()
    # test_fast_hadamard()