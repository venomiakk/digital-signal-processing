from signals import SignalObject, SignalOperations, SignalGenerator
from plots import plot_points, plot_signal, plot_sampling, plot_reconstructed_signal, plot_quantization
from converter import SignalConverter


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

class ConverterExperiments:
    @staticmethod
    def experiment_sinus1():        
        signal1 = SignalGenerator.sin_signal(A=1, T=0.5, t_start=0, d=2, sampling_rate=1000)
        for i in range(4,9):
            print(f"n_bits: {i}")
            quant_trunc_signal = SignalConverter.quantization_with_truncation(signal1.time, signal1.signal, n_bits=i)
            print(f"MSE: {SignalConverter.mse(signal1.signal, quant_trunc_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, quant_trunc_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, quant_trunc_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, quant_trunc_signal):.6f}")
            print(f"ENOB: {SignalConverter.enob(signal1.signal, quant_trunc_signal):.6f}")
            plot_quantization(f"Kwantyzacja z obcięciem, {i} bity", signal1, quant_trunc_signal[0], quant_trunc_signal[1], toplot=True)
        for i in range(4,9):
            print(f"n_bits: {i}")
            quant_round_signal = SignalConverter.quantization_with_rounding(signal1.time, signal1.signal, n_bits=i)
            print(f"MSE: {SignalConverter.mse(signal1.signal, quant_round_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, quant_round_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, quant_round_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, quant_round_signal):.6f}")
            print(f"ENOB: {SignalConverter.enob(signal1.signal, quant_round_signal):.6f}")
            plot_quantization(f"Kwantyzacja z zaokrągleniem, {i} bity", signal1, quant_round_signal[0], quant_round_signal[1], toplot=True)
    @staticmethod
    def experiment_sinus2():
        signal1 = SignalGenerator.sin_signal(A=1, T=0.5, t_start=0, d=2, sampling_rate=1000)
        fs_rates = [10, 20, 50, 100]
        for fs in fs_rates:
            print(f"fs: {fs}")
            sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=fs)
            reconstructed_signal = SignalConverter.zero_order_hold(signal1.time, sampled_time, sampled_values)
            print(f"MSE: {SignalConverter.mse(signal1.signal, reconstructed_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, reconstructed_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, reconstructed_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, reconstructed_signal):.6f}")
            plot_reconstructed_signal(f"Ekstrapolacja zerowego rzędu, fs={fs}", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)
        for fs in fs_rates:
            print(f"fs: {fs}")
            sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=fs)
            reconstructed_signal = SignalConverter.first_order_hold(signal1.time, sampled_time, sampled_values)
            print(f"MSE: {SignalConverter.mse(signal1.signal, reconstructed_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, reconstructed_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, reconstructed_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, reconstructed_signal):.6f}")
            plot_reconstructed_signal(f"Interpolacja pierwszego rzędu, fs={fs}", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)
        for fs in fs_rates:
            print(f"fs: {fs}")
            sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=fs)
            reconstructed_signal = SignalConverter.sinc_interpolation(signal1.time, sampled_time, sampled_values)
            print(f"MSE: {SignalConverter.mse(signal1.signal, reconstructed_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, reconstructed_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, reconstructed_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, reconstructed_signal):.6f}")
            plot_reconstructed_signal(f"Interpolacja funkcją sinc, fs={fs}", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)
    @staticmethod
    def experiment_tri3():
        signal1 = SignalGenerator.triangle_signal(A=1, T=0.5, kw=1, t_start=0, d=2, sampling_rate=1000)
        for i in range(4,9):
            print(f"n_bits: {i}")
            quant_trunc_signal = SignalConverter.quantization_with_truncation(signal1.time, signal1.signal, n_bits=i)
            print(f"MSE: {SignalConverter.mse(signal1.signal, quant_trunc_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, quant_trunc_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, quant_trunc_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, quant_trunc_signal):.6f}")
            plot_quantization(f"Kwantyzacja z obcięciem, {i} bity", signal1, quant_trunc_signal[0], quant_trunc_signal[1], toplot=True)
        for i in range(4,9):
            print(f"n_bits: {i}")
            quant_round_signal = SignalConverter.quantization_with_rounding(signal1.time, signal1.signal, n_bits=i)
            print(f"MSE: {SignalConverter.mse(signal1.signal, quant_round_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, quant_round_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, quant_round_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, quant_round_signal):.6f}")
            plot_quantization(f"Kwantyzacja z zaokrągleniem, {i} bity", signal1, quant_round_signal[0], quant_round_signal[1], toplot=True)

    @staticmethod
    def experiment_tri4():
        signal1 = SignalGenerator.triangle_signal(A=1, T=0.5, kw=1, t_start=0, d=2, sampling_rate=1000)
        fs_rates = [10, 20, 50, 100]
        for fs in fs_rates:
            print(f"fs: {fs}")
            sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=fs)
            reconstructed_signal = SignalConverter.zero_order_hold(signal1.time, sampled_time, sampled_values)
            print(f"MSE: {SignalConverter.mse(signal1.signal, reconstructed_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, reconstructed_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, reconstructed_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, reconstructed_signal):.6f}")
            plot_reconstructed_signal(f"Ekstrapolacja zerowego rzędu, fs={fs}", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)
        for fs in fs_rates:
            print(f"fs: {fs}")
            sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=fs)
            reconstructed_signal = SignalConverter.first_order_hold(signal1.time, sampled_time, sampled_values)
            print(f"MSE: {SignalConverter.mse(signal1.signal, reconstructed_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, reconstructed_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, reconstructed_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, reconstructed_signal):.6f}")
            plot_reconstructed_signal(f"Interpolacja pierwszego rzędu, fs={fs}", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)
        for fs in fs_rates:
            print(f"fs: {fs}")
            sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=fs)
            reconstructed_signal = SignalConverter.sinc_interpolation(signal1.time, sampled_time, sampled_values)
            print(f"MSE: {SignalConverter.mse(signal1.signal, reconstructed_signal):.6f}")
            print(f"SNR: {SignalConverter.snr(signal1.signal, reconstructed_signal):.6f}")
            print(f"PSNR: {SignalConverter.psnr(signal1.signal, reconstructed_signal):.6f}")
            print(f"MD: {SignalConverter.md(signal1.signal, reconstructed_signal):.6f}")
            plot_reconstructed_signal(f"Interpolacja funkcją sinc, fs={fs}", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)

    @staticmethod
    def aliasing_experiment():
        signal1 = SignalGenerator.sin_signal(A=2, T=0.001, t_start=0, d=0.01, sampling_rate=1000000)
        sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=1200)
        plot_sampling("Próbkowanie", signal1, sampled_time, sampled_values, toplot=True)
        signal1 = SignalGenerator.sin_signal(A=2, T=0.005, t_start=0, d=0.04, sampling_rate=1000000)
        sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=300)
        plot_sampling("Próbkowanie", signal1, sampled_time, sampled_values, toplot=True)
if __name__ == "__main__":
    # ConverterExperiments.experiment_sinus1()
    # ConverterExperiments.experiment_sinus2()
    # ConverterExperiments.experiment_tri3()
    # ConverterExperiments.experiment_tri4()
    ConverterExperiments.aliasing_experiment()