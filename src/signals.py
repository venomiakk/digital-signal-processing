import numpy as np
from plots import plot_signal, plot_points

class SignalObject:
    def __init__(self, signal, time, sampling_rate=None, A=None, T=None, t_start=None, d=None, kw=None,
                  n_start=None, n_spike=None, p=None, discrete_signal=False):
        self.signal = signal
        self.time = time

        # TODO: different calculations for periodic signals?
        self.mean_value = np.mean(signal)
        self.abs_mean_value = np.mean(np.abs(signal))
        self.rms_value = np.sqrt(np.mean(np.square(signal)))
        self.variance = np.var(signal)
        self.avg_power = np.mean(np.square(signal))

        self.sampling_rate = sampling_rate
        self.A = A
        self.T = T
        self.t_start = t_start
        self.d = d
        self.kw = kw
        self.n_start = n_start
        self.n_spike = n_spike
        self.p = p

        self.discrete_signal = discrete_signal

class SignalGenerator:
    @staticmethod
    def uniformly_distributed_noise(A=1, t_start=0, d=2, sampling_rate=1000):
        # S1
        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = np.random.uniform(-A, A, len(time))

        sigObj = SignalObject(signal, time, sampling_rate, A=A, t_start=t_start, d=d)
        return sigObj

    @staticmethod
    def gaussian_noise(A=1, t_start=0, d=2, sampling_rate=1000):
        # S2
        #TODO: make amplitude A to be from -A to A
        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = np.random.normal(0, 1, len(time))
        minS = np.min(signal)
        maxS = np.max(signal)
        signal = A * (signal - minS) / (maxS - minS)
        sigObj = SignalObject(signal, time, sampling_rate, A=A, t_start=t_start, d=d)
        return sigObj

    @staticmethod
    def sin_signal(A=1, T=1, t_start=0, d=2, sampling_rate=1000):
        # S3
        # TODO: Check if this is correct
        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = A * np.sin(2 * np.pi * (time - t_start) / T)

        sigObj = SignalObject(signal, time, sampling_rate, A=A, T=T, t_start=t_start, d=d)
        return sigObj

    @staticmethod
    def sin_half_signal(A=1, T=1, t_start=0, d=2, sampling_rate=1000):
        # S4

        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = 0.5 * A * ((np.sin(2 * np.pi * (time - t_start) / T)) + np.abs(np.sin(2 * np.pi * (time - t_start) / T)))

        sigObj = SignalObject(signal, time, sampling_rate, A=A, T=T, t_start=t_start, d=d)
        return sigObj

    @staticmethod
    def sin_twohalf_signal(A=1, T=1, t_start=0, d=2, sampling_rate=1000):
        # S5
        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = A * np.abs(np.sin(2 * np.pi * (time - t_start) / T))

        sigObj = SignalObject(signal, time, sampling_rate, A=A, T=T, t_start=t_start, d=d)
        return sigObj

    @staticmethod
    def square_signal(A=1, T=1, kw=0.5, t_start=0, d=2, sampling_rate=1000):
        # TODO: Check if this is correct
        # S6

        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = np.zeros_like(time)

        for i, t in enumerate(time):
            k = np.floor(t / T)  # Numer okresu
            t_mod = t - k * T  # Czas w bieżącym okresie
            
            if t_start <= t_mod < kw * T + t_start:
                signal[i] = A
            elif kw * T + t_start <= t_mod < T + t_start:
                signal[i] = 0

        sigObj = SignalObject(signal, time, sampling_rate, A=A, T=T, t_start=t_start, d=d, kw=kw)
        return sigObj

    @staticmethod
    def square_symmetric_signal(A=1, T=1, kw=0.5, t_start=0, d=2, sampling_rate=1000):
        # S7
        # TODO: Check if this is correct
        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = np.zeros_like(time)

        for i, t in enumerate(time):
            k = np.floor(t / T)  # Numer okresu
            t_mod = t - k * T  # Czas w bieżącym okresie
            
            if t_start <= t_mod < kw * T + t_start:
                signal[i] = A
            elif kw * T + t_start <= t_mod < T + t_start:
                signal[i] = -A

        sigObj = SignalObject(signal, time, sampling_rate, A=A, T=T, t_start=t_start, d=d, kw=kw)
        return sigObj

    @staticmethod
    def triangle_signal(A=1, T=1, t_start=0, d=2, kw=0.5, sampling_rate=1000):
        # S8
        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = np.zeros_like(time)

        for i, t in enumerate(time):
            k = np.floor(t / T)  # Numer okresu
            t_mod = t - k * T  # Czas w bieżącym okresie
            
            if t_start <= t_mod < kw * T + t_start:
                signal[i] = (A / (kw * T)) * (t_mod - t_start)
            elif kw * T + t_start <= t_mod < T + t_start:
                signal[i] = (-A / (T * (1 - kw))) * (t_mod - t_start) + A / (1 - kw)

        sigObj = SignalObject(signal, time, sampling_rate, A=A, T=T, t_start=t_start, d=d, kw=kw)
        return sigObj

    @staticmethod
    def step_signal(A=1, t_start=0, d=2, sampling_rate=1000):
        # S9
        # Czas trwania sygnału w sekundach
        t_end = t_start + d
        t_step = t_end / 2

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = np.piecewise(time, [time < t_step, time >= t_step], [0, A])

        sigObj = SignalObject(signal, time, sampling_rate, A=A, t_start=t_start, d=d)
        return sigObj

    @staticmethod
    def unit_impulse(A=1, n_start=0, n_spike = 10, sampling_rate=10, d=2):
        # S10
        time = np.linspace(0, d, int(d * sampling_rate))
        signal = np.zeros_like(time)
        if n_spike < len(signal):
            signal[n_spike] = A
        else:
            signal[-1] = A

        sigObj = SignalObject(signal, time, sampling_rate, A=A, n_start=n_start, n_spike=n_spike, discrete_signal=True)
        return sigObj

    @staticmethod
    def impulse_noise(A=1, t_start=0, d=2, sampling_rate=30, p=0.5):
        # S11
        # TODO: Check if this is correct
        t_end = t_start + d

        time = np.linspace(0, t_end, int(d * sampling_rate))
        signal = np.random.choice([0, A], len(time), p=[1-p, p])

        sigObj = SignalObject(signal, time, sampling_rate, A=A, t_start=t_start, d=d, p=p, discrete_signal=True)
        return sigObj

class SignalOperations:
    @staticmethod
    def add_signals(signal1, signal2):
        new_signal = signal1.signal + signal2.signal
        new_time = signal1.time
        new_sampling_rate = signal1.sampling_rate

        return SignalObject(new_signal, new_time, sampling_rate=new_sampling_rate)

    @staticmethod
    def subtract_signals(signal1, signal2):
        new_signal = signal1.signal - signal2.signal
        new_time = signal1.time
        new_sampling_rate = signal1.sampling_rate

        return SignalObject(new_signal, new_time, sampling_rate=new_sampling_rate)

    @staticmethod
    def multiply_signals(signal1, signal2):
        new_signal = signal1.signal * signal2.signal
        new_time = signal1.time
        new_sampling_rate = signal1.sampling_rate

        return SignalObject(new_signal, new_time, sampling_rate=new_sampling_rate)

    @staticmethod
    def divide_signals(signal1, signal2):
        # TODO: different epsilon?
        epsilon = 0.1
        new_signal = signal1.signal / (signal2.signal + epsilon)
        new_time = signal1.time
        new_sampling_rate = signal1.sampling_rate

        return SignalObject(new_signal, new_time, sampling_rate=new_sampling_rate)

if __name__ == "__main__":
    # SignalGenerator.uniformly_distributed_noise()
    # gaussian_noise()
    # sin_signal()
    # sin_half_signal()
    # sin_twohalf_signal()
    # square_signal()
    # SignalGenerator.square_symmetric_signal()
    # triangle_signal()
    # step_signal()
    # unit_impulse()
    # SignalGenerator.impulse_noise()
    s1 = SignalGenerator.sin_signal()
    s2 = SignalGenerator.square_signal()
    SignalOperations.divide_signals(s1, s2)