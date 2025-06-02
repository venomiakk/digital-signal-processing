from signals import SignalGenerator, SignalOperations
import matplotlib.pyplot as plt
import numpy as np
from filters import CustomSignalFilters

if __name__ == "__main__":
    # Example usage
    sin = SignalGenerator.sin_signal(A=1, T=1)
    noise = SignalGenerator.gaussian_noise(A=1,)

    conv = np.convolve(sin.signal, noise.signal, mode='full')

    conv2 = CustomSignalFilters.convolve(sin.signal, noise.signal)

    plt.figure(figsize=(8, 10))
    plt.subplot(3, 1, 1)
    plt.plot(sin.time, sin.signal, label='Sine Wave')
    plt.subplot(3, 1, 2)
    plt.plot(noise.time, noise.signal, label='Gaussian Noise')
    plt.subplot(3, 1, 3)
    plt.plot(conv, label='Convolution Result')
    plt.show()

    plt.figure(figsize=(8, 10))
    plt.subplot(3, 1, 1)
    plt.plot(sin.time, sin.signal, label='Sine Wave')
    plt.subplot(3, 1, 2)
    plt.plot(noise.time, noise.signal, label='Gaussian Noise')
    plt.subplot(3, 1, 3)
    plt.plot(conv2, label='Custom Convolution Result')
    plt.show()