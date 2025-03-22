from signals import SignalObject, SignalOperations, SignalGenerator
from plots import plot_points, plot_signal

def experiment1():
    # SignalGenerator.uniformly_distributed_noise()
    signal1 = SignalGenerator.uniformly_distributed_noise(A=1, t_start=0, d=2, sampling_rate=1000)
    plot_signal(signal1, toplot=True)

    signal2 = SignalGenerator.gaussian_noise(A=1, t_start=0, d=2, sampling_rate=1000)
    plot_signal(signal2, toplot=True)
    

if __name__ == "__main__":
    experiment1()