import numpy as np
import matplotlib.pyplot as plt
from signals import SignalGenerator, SignalObject, SignalOperations
from plots import plot_signal, plot_points
from scipy import signal as spsignal


class SignalFilters:
    @staticmethod
    def convolve(signal1, signal2, mode='full'):
        """
        Perform convolution between two signals.
        
        Parameters:
            signal1: SignalObject - first signal
            signal2: SignalObject - second signal (kernel)
            mode: string - 'full', 'same', or 'valid' (numpy.convolve modes)
        
        Returns:
            SignalObject with the convolved signal
        """
        convolved = np.convolve(signal1.signal, signal2.signal, mode=mode)
        
        # Create appropriate time array based on mode
        if mode == 'full':
            dt = signal1.time[1] - signal1.time[0]
            new_time = np.arange(
                signal1.time[0] + signal2.time[0],
                signal1.time[0] + signal2.time[0] + len(convolved) * dt,
                dt
            )
        elif mode == 'same':
            new_time = signal1.time.copy()
        else:  # valid
            new_time = signal1.time[:len(convolved)]
            
        return SignalObject(convolved, new_time, sampling_rate=signal1.sampling_rate)
    
    @staticmethod
    def correlate(signal1, signal2, mode='full'):
        """
        Compute correlation between two signals.
        
        Parameters:
            signal1: SignalObject - first signal
            signal2: SignalObject - second signal
            mode: string - 'full', 'same', or 'valid' (numpy.correlate modes)
            
        Returns:
            SignalObject with the correlation result
        """
        correlation = np.correlate(signal1.signal, signal2.signal, mode=mode)
        
        # Create appropriate time array
        if mode == 'full':
            dt = signal1.time[1] - signal1.time[0]
            new_time = np.arange(
                signal1.time[0] - signal2.time[-1] + signal2.time[0],
                signal1.time[0] - signal2.time[-1] + signal2.time[0] + len(correlation) * dt,
                dt
            )
        elif mode == 'same':
            new_time = signal1.time.copy()
        else:  # valid
            new_time = signal1.time[:len(correlation)]
            
        return SignalObject(correlation, new_time, sampling_rate=signal1.sampling_rate)
    
    @staticmethod
    def low_pass_filter(signal, cutoff_freq, filter_order=5):
        """
        Apply a low-pass filter to the signal.
        
        Parameters:
            signal: SignalObject - the signal to filter
            cutoff_freq: float - cutoff frequency in Hz
            filter_order: int - order of the Butterworth filter
            
        Returns:
            SignalObject with the filtered signal
        """
        
        
        # Calculate Nyquist frequency
        fs = signal.sampling_rate
        nyquist = 0.5 * fs
        
        # Normalized cutoff frequency
        normal_cutoff = cutoff_freq / nyquist
        
        # Get filter coefficients
        b, a = spsignal.butter(filter_order, normal_cutoff, btype='low')
        
        # Apply filter
        filtered_signal = spsignal.filtfilt(b, a, signal.signal)
        
        return SignalObject(filtered_signal, signal.time, sampling_rate=fs)
    
    @staticmethod
    def high_pass_filter(signal, cutoff_freq, filter_order=5):
        """
        Apply a high-pass filter to the signal.
        
        Parameters:
            signal: SignalObject - the signal to filter
            cutoff_freq: float - cutoff frequency in Hz
            filter_order: int - order of the Butterworth filter
            
        Returns:
            SignalObject with the filtered signal
        """
        
        # Calculate Nyquist frequency
        fs = signal.sampling_rate
        nyquist = 0.5 * fs
        
        # Normalized cutoff frequency
        normal_cutoff = cutoff_freq / nyquist
        
        # Get filter coefficients
        b, a = spsignal.butter(filter_order, normal_cutoff, btype='high')
        
        # Apply filter
        filtered_signal = spsignal.filtfilt(b, a, signal.signal)
        
        return SignalObject(filtered_signal, signal.time, sampling_rate=fs)

# Example usage
if __name__ == "__main__":
    # Create test signals
    t_duration = 2
    fs = 1000  # sampling frequency
    
    # Create a signal with multiple frequency components
    signal1 = SignalGenerator.sin_signal(A=1, T=0.1, d=t_duration, sampling_rate=fs)  # 10 Hz sine wave
    signal2 = SignalGenerator.sin_signal(A=0.5, T=0.02, d=t_duration, sampling_rate=fs)  # 50 Hz sine wave
    
    # Combine signals
    mixed_signal = SignalOperations.add_signals(signal1, signal2)
    
    # Apply filters
    low_passed = SignalFilters.low_pass_filter(mixed_signal, cutoff_freq=20)
    high_passed = SignalFilters.high_pass_filter(mixed_signal, cutoff_freq=20)
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    plt.subplot(4, 1, 1)
    plt.plot(mixed_signal.time, mixed_signal.signal)
    plt.title('Original Mixed Signal (10 Hz + 50 Hz)')
    plt.grid(True)
    
    plt.subplot(4, 1, 2)
    plt.plot(low_passed.time, low_passed.signal)
    plt.title('Low-Pass Filtered Signal (< 20 Hz)')
    plt.grid(True)
    
    plt.subplot(4, 1, 3)
    plt.plot(high_passed.time, high_passed.signal)
    plt.title('High-Pass Filtered Signal (> 20 Hz)')
    plt.grid(True)
    
    # Correlation example
    plt.subplot(4, 1, 4)
    corr = SignalFilters.correlate(signal1, signal2, mode='same')
    plt.plot(corr.time, corr.signal)
    plt.title('Correlation between 10 Hz and 50 Hz Signals')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Convolution example
    plt.figure(figsize=(10, 6))

    # Create a simple kernel (e.g., moving average filter)
    kernel_time = np.linspace(0, 0.1, 100)
    kernel_signal = np.ones(len(kernel_time)) / len(kernel_time)  # Normalized box filter
    kernel = SignalObject(kernel_signal, kernel_time, sampling_rate=fs)

    # Apply convolution
    convolved = SignalFilters.convolve(mixed_signal, kernel, mode='same')

    # Plot original and convolved signal
    plt.subplot(2, 1, 1)
    plt.plot(mixed_signal.time, mixed_signal.signal)
    plt.title('Original Mixed Signal')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(convolved.time, convolved.signal)
    plt.title('Convolved Signal (Moving Average Smoothing)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()