import numpy as np
from plots import plot_signal


def uniformly_distributed_noise():
    # S1

    # parameters
    A = 1           # amplitude 
    t_start = 0     # start time
    d = 2           # duration
    t_end = t_start + d
    sampling_rate = 1000  # Próbkowanie

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.random.uniform(-A, A, len(time))
    
    plot_signal(signal, time)

    return signal, time

def gaussian_noise():
    # TODO: czy trzeba skorzystac ze wzoru na rozkald normalny czy mozna tak jak nizej?
    # S2
    # parameters
    A = 1           # amplitude 
    t_start = 0     # start time
    d = 2           # duration
    t_end = t_start + d
    sampling_rate = 1000  # Próbkowanie

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = A * np.random.normal(0, 1, len(time))
    
    plot_signal(signal, time)

    return signal, time

def sin_signal():
    # TODO: Check if this is correct
    # S3
    A = 1       # Amplituda
    T = 1.0       # Okres (np. 1 sekunda, co oznacza częstotliwość 1 Hz)
    t_start = 0      # start time
    d = 2       # Czas trwania sygnału w sekundach
    t_end = t_start + d
    sampling_rate = 1000  # Próbkowanie

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = A * np.sin(2 * np.pi * (time - t_start) / T)

    plot_signal(signal, time)

    return signal, time

def sin_half_signal():
    # S4

    A = 1       # Amplituda
    T = 1       # Okres (np. 1 sekunda, co oznacza częstotliwość 1 Hz)
    t_start = 0      # start time
    d = 2       # Czas trwania sygnału w sekundach
    t_end = t_start + d
    sampling_rate = 1000  # Próbkowanie

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = 0.5 * A * ((np.sin(2 * np.pi * (time - t_start) / T)) + np.abs(np.sin(2 * np.pi * (time - t_start) / T)))

    plot_signal(signal, time)

    return signal, time

def sin_twohalf_signal():
    # S5
    A = 1       # Amplituda
    T = 1.0       # Okres (np. 1 sekunda, co oznacza częstotliwość 1 Hz)
    t_start = 0      # start time
    d = 2       # Czas trwania sygnału w sekundach
    t_end = t_start + d
    sampling_rate = 1000  # Próbkowanie

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = A * np.abs(np.sin(2 * np.pi * (time - t_start) / T))

    plot_signal(signal, time)

    return signal, time

def square_signal():
    # TODO: Check if this is correct
    # S6
    A = 1       # Amplituda
    T = 1.0       # Okres (np. 1 sekunda, co oznacza częstotliwość 1 Hz)
    kw = 0.35   # Współczynnik wypełnienia
    t_start = 0      # start time
    d = 2       # Czas trwania sygnału w sekundach
    t_end = t_start + d
    sampling_rate = 1000  # Próbkowanie

    time = np.linspace(0, t_end, int(d * sampling_rate))

    signal = np.zeros_like(time)
    cycles = int(T * sampling_rate)
    high_cycles = int(cycles * kw)

    for k in range(int(len(time) / cycles) + 1):
        start_idx = int(k * cycles)
        end_idx = min(start_idx + high_cycles, len(time))
        signal[start_idx:end_idx] = A
        
        start_low_idx = end_idx
        end_low_idx = min(start_low_idx + (cycles - high_cycles), len(time))
        signal[start_low_idx:end_low_idx] = -A
    
    plot_signal(signal, time)

    return signal, time

def square_symmetric_signal():
    # S7
    pass

def triangle_signal():
    # S8
    pass

def step_signal():
    # S9
    A = 1       # Amplituda
    t_start = 0      # start time
    d = 2       # Czas trwania sygnału w sekundach
    t_end = t_start + d
    t_step = t_end / 2
    sampling_rate = 1000  # Próbkowanie

    time = np.linspace(0, t_end, int(d * sampling_rate))
    signal = np.piecewise(time, [time < t_step, time >= t_step], [0, A])
    
    plot_signal(signal, time)

    return signal, time

def unit_impulse():
    # S10
    pass

def impulse_noise():
    # S11
    pass

if __name__ == "__main__":
    # uniformly_distributed_noise()
    # gaussian_noise()
    # sin_signal()
    # sin_half_signal()
    # sin_twohalf_signal()
    square_signal()
    # square_symmetric_signal()
    # triangle_signal()
    # step_signal()
    # unit_impulse()
    # impulse_noise()