from signals import SignalObject, SignalOperations, SignalGenerator
from plots import plot_points, plot_signal

def experiment1():
    # signal1 = SignalGenerator.uniformly_distributed_noise(A=1, t_start=0, d=2, sampling_rate=1000)
    # plot_signal(signal1, toplot=True)

    signal2 = SignalGenerator.gaussian_noise(A=1, t_start=0, d=2, sampling_rate=1000)
    plot_signal(signal2, toplot=True)

    # signal3 = SignalGenerator.sin_signal(A=1, T=1, t_start=0, d=2, sampling_rate=1000)
    # plot_signal(signal3, toplot=True)

    # signal4 = SignalGenerator.sin_half_signal(A=2, T=1, t_start=1, d=2, sampling_rate=1000)
    # plot_signal(signal4, toplot=True)

    signal5 = SignalGenerator.sin_twohalf_signal(A=2, T=2, t_start=1.5, d=2, sampling_rate=1000)
    plot_signal(signal5, toplot=True)

    # signal6 = SignalGenerator.square_signal(A=1, T=2, kw=0.75, t_start=1.5, d=4, sampling_rate=1000)
    # plot_signal(signal6, toplot=True)

    # signal7 = SignalGenerator.square_symmetric_signal(A=1, T=2, kw=0.75, t_start=2, d=4, sampling_rate=1000)
    # plot_signal(signal7, toplot=True)

    signal8 = SignalGenerator.triangle_signal(A=1, T=2, kw=1, t_start=1, d=4, sampling_rate=1000)
    plot_signal(signal8, toplot=True)

    # signal9 = SignalGenerator.step_signal(A=1, t_start=-5, d=10, t_step=2, sampling_rate=1000)
    # plot_signal(signal9, toplot=True)

    # signal10 = SignalGenerator.unit_impulse(A=1, t_start=-1, d=2, sampling_rate=10, n_spike=10)
    # plot_points(signal10, toplot=True)

    signal11 = SignalGenerator.impulse_noise(A=2, t_start=1, d=2, sampling_rate=10, p=0.5)
    plot_points(signal11, toplot=True)

    pass
    

def experiment2():
    signal1 = SignalGenerator.sin_signal(A=1, T=1, t_start=0, d=4, sampling_rate=1000)
    signal2 = SignalGenerator.square_signal(A=1, T=2, kw=0.5, t_start=0, d=4, sampling_rate=1000)
    plot_signal(signal1, toplot=True)
    plot_signal(signal2, toplot=True)

    # signal_add = SignalOperations.add_signals(signal1, signal2)
    # plot_signal(signal_add, toplot=True)

    # signal_sub = SignalOperations.subtract_signals(signal1, signal2)
    # plot_signal(signal_sub, toplot=True)

    # signal_mul = SignalOperations.multiply_signals(signal1, signal2)
    # plot_signal(signal_mul, toplot=True)

    signal_div = SignalOperations.divide_signals(signal1, signal2)
    plot_signal(signal_div, toplot=True)

if __name__ == "__main__":
    experiment1()
    # experiment2()