import numpy as np

from signals import SignalObject, SignalOperations, SignalGenerator
from plots import plot_points, plot_signal, plot_sampling, plot_reconstructed_signal, plot_quantization, plot_filters
from converter import SignalConverter
from src.filters import CustomSignalFilters
import matplotlib.pyplot as plt
import numpy as np
import os


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
        sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=450)
        plot_sampling("Próbkowanie", signal1, sampled_time, sampled_values, toplot=True)
        reconstructed_signal = SignalConverter.sinc_interpolation(signal1.time, sampled_time, sampled_values)
        plot_reconstructed_signal("Rekonstrukcja", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)
        signal1 = SignalGenerator.sin_signal(A=2, T=0.005, t_start=0, d=0.04, sampling_rate=1000000)
        sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=70)
        plot_sampling("Próbkowanie", signal1, sampled_time, sampled_values, toplot=True)
        reconstructed_signal = SignalConverter.sinc_interpolation(signal1.time, sampled_time, sampled_values)
        plot_reconstructed_signal("Rekonstrukcja", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)

    @staticmethod
    def test_exp():
        signal1 = SignalGenerator.sin_signal(A=1, T=0.5, t_start=0, d=2, sampling_rate=1000)
        qt1, q1 = SignalConverter.quantization_with_truncation(signal1.time, signal1.signal, n_bits=4)
        qt1, q2 = SignalConverter.quantization_with_rounding(signal1.time, signal1.signal, n_bits=4)

        sampled_time, sampled_values = SignalConverter.sample_signal(signal1.signal, signal1.time, fs=10)
        reconstructed_signal = SignalConverter.zero_order_hold(signal1.time, sampled_time, sampled_values)
        reconstructed_signal2 = SignalConverter.first_order_hold(signal1.time, sampled_time, sampled_values)
        reconstructed_signal3 = SignalConverter.sinc_interpolation(signal1.time, sampled_time, sampled_values)

        plot_reconstructed_signal("Rekonstrukcja", signal1.signal, signal1.time, sampled_values, sampled_time, reconstructed_signal, toplot=True)

    @staticmethod
    def filters_test():

        # Define signal parameters
        sampling_rate = 1000
        duration = 2
        amplitude = 1
        period = 1

        # Generate a sinusoidal signal
        signal = SignalGenerator.sin_signal(A=amplitude, T=period, d=duration, sampling_rate=sampling_rate)
        original_signal = signal.signal
        time = signal.time

        # Add Gaussian noise
        noisy_signal = original_signal + 0.2 * np.random.normal(0, 1, len(original_signal))

        # Define filter types and window functions
        filter_types = ['low', 'high', 'band']
        window_functions = {
            "Hamming": CustomSignalFilters.apply_hamming_window,
            "Hanning": CustomSignalFilters.apply_hanning_window,
            "Blackman": CustomSignalFilters.apply_blackman_window,
        }

        # Define filter parameters to test
        cutoff_frequencies = [10, 20, 100]  # Example cutoff frequencies
        filter_orders = [10, 20, 30]  # Example filter orders

        # Create output directory for plots
        output_dir = "filter_plots"
        os.makedirs(output_dir, exist_ok=True)

        # Test each combination of filter type, window, cutoff frequency, and filter order
        for filter_type in filter_types:
            for window_name, window_func in window_functions.items():
                for cutoff_freq in cutoff_frequencies:
                    for filter_order in filter_orders:
                        # Apply filter and window
                        filter_response = CustomSignalFilters.aplly_filter(
                            noisy_signal, cutoff_freq=cutoff_freq, filter_order=filter_order, filter_type=filter_type
                        )
                        filtered_signal = window_func(filter_response)

                        # Plot results on the same plot
                        plt.figure(figsize=(10, 6))
                        plt.plot(time, original_signal, label="Original Signal", color="blue", alpha=0.7)
                        plt.plot(time, noisy_signal, label="Noisy Signal (Gaussian)", color="orange", alpha=0.7)
                        plt.plot(time, filtered_signal[:len(time)],
                                 label=f"Filtered Signal ({filter_type.capitalize()} - {window_name})", color="green",
                                 alpha=0.7)

                        # Add filter parameters as text on the plot
                        filter_params_text = (
                            f"Filter Type: {filter_type.capitalize()}\n"
                            f"Window: {window_name}\n"
                            f"Cutoff Frequency: {cutoff_freq} Hz\n"
                            f"Filter Order: {filter_order}"
                        )
                        plt.text(0.02, 0.95, filter_params_text, transform=plt.gca().transAxes,
                                 fontsize=10, verticalalignment='top',
                                 bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))

                        plt.title(f"Filter Test: {filter_type.capitalize()} Filter ({window_name} Window)")
                        plt.xlabel("Time [s]")
                        plt.ylabel("Amplitude")
                        plt.legend()
                        plt.grid()
                        plt.tight_layout()

                        # Save the plot as an image
                        filename = f"{filter_type}_{window_name}_cutoff{cutoff_freq}_order{filter_order}.png"
                        filepath = os.path.join(output_dir, filename)
                        plt.savefig(filepath)
                        plt.close()

        print(f"Plots saved in directory: {output_dir}")

    @staticmethod
    def experiment_convolution():
        # Define signal combinations
        signal_combinations = [
            (SignalGenerator.sin_signal(A=1, T=1, t_start=0, d=4, sampling_rate=1000),
             SignalGenerator.sin_signal(A=2, T=1, t_start=0.5, d=4, sampling_rate=1000)),
            (SignalGenerator.triangle_signal(A=1, T=2, kw=0.5, t_start=0, d=4, sampling_rate=1000),
             SignalGenerator.square_symmetric_signal(A=1, T=2, kw=0.75, t_start=0, d=4, sampling_rate=1000)),
            (SignalGenerator.gaussian_noise(A=1, t_start=0, d=4, sampling_rate=1000),
             SignalGenerator.sin_signal(A=1, T=1, t_start=0, d=4, sampling_rate=1000)),
            (SignalGenerator.square_symmetric_signal(A=1, T=2, kw=0.75, t_start=0, d=4, sampling_rate=1000),
             SignalGenerator.sin_signal(A=1, T=1.5, t_start=0.5, d=4, sampling_rate=1000)),
        ]

        # Iterate through signal combinations
        for i, (signal1, signal2) in enumerate(signal_combinations):
            # Extract signal data
            time1, values1 = signal1.time, signal1.signal
            time2, values2 = signal2.time, signal2.signal

            # Compute convolution
            convolved_values = CustomSignalFilters.convolve(values1, values2)
            convolved_time = np.linspace(time1[0], time1[0] + len(convolved_values) / signal1.sampling_rate,
                                         len(convolved_values))

            # Generate titles with signal metadata
            title1 = f"Signal 1:(A={signal1.A}, T={signal1.T}, t_start={signal1.t_start}, d={signal1.d})"
            title2 = f"Signal 2:(A={signal2.A}, T={signal2.T}, t_start={signal2.t_start}, d={signal2.d})"
            title3 = f"Convolution of Signal 1 and Signal 2"

            # Plot the signals and their convolution
            fig, ax = plt.subplots(3, 1, figsize=(10, 8))
            ax[0].plot(time1, values1, label="Signal 1", linewidth=1.5)
            ax[0].set_title(title1)
            ax[0].grid()

            ax[1].plot(time2, values2, label="Signal 2", linewidth=1.5)
            ax[1].set_title(title2)
            ax[1].grid()

            ax[2].plot(convolved_time, convolved_values, label="Convolution", linewidth=1.5, linestyle="--")
            ax[2].set_title(title3)
            ax[2].grid()

            plt.tight_layout()
            plt.show()

    @staticmethod
    def experiment_correlation():
        signal_combinations = [
            (SignalGenerator.sin_signal(A=1, T=1, t_start=0, d=4, sampling_rate=1000),
             SignalGenerator.sin_signal(A=2, T=1, t_start=0.5, d=4, sampling_rate=1000)),
            (SignalGenerator.triangle_signal(A=1, T=2, kw=0.5, t_start=0, d=4, sampling_rate=1000),
             SignalGenerator.square_symmetric_signal(A=1, T=2, kw=0.75, t_start=0, d=4, sampling_rate=1000)),
            (SignalGenerator.square_symmetric_signal(A=1, T=2, kw=0.75, t_start=0, d=4, sampling_rate=1000),
             SignalGenerator.sin_signal(A=1, T=1.5, t_start=0.5, d=4, sampling_rate=1000)),
        ]

        # Iterate through signal combinations
        for i, (signal1, signal2) in enumerate(signal_combinations):
            # Extract signal data
            time1, values1 = signal1.time, signal1.signal
            time2, values2 = signal2.time, signal2.signal

            # Compute convolution
            correleted_values = CustomSignalFilters.correlation_via_convolution(values1, values2)
            corelleted_time = np.arange(-(len(values2)-1), len(values1)) / signal1.sampling_rate

            # Generate titles with signal metadata
            title1 = f"Signal 1:(A={signal1.A}, T={signal1.T}, t_start={signal1.t_start}, d={signal1.d})"
            title2 = f"Signal 2:(A={signal2.A}, T={signal2.T}, t_start={signal2.t_start}, d={signal2.d})"
            title3 = f"Correlation of Signal 1 and Signal 2"

            # Plot the signals and their convolution
            fig, ax = plt.subplots(3, 1, figsize=(10, 8))
            ax[0].plot(time1, values1, label="Signal 1", linewidth=1.5)
            ax[0].set_title(title1)
            ax[0].grid()

            ax[1].plot(time2, values2, label="Signal 2", linewidth=1.5)
            ax[1].set_title(title2)
            ax[1].grid()

            ax[2].plot(corelleted_time, correleted_values, label="Convolution", linewidth=1.5, linestyle="--")
            ax[2].set_title(title3)
            ax[2].grid()

            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    # ConverterExperiments.experiment_sinus1()
    # ConverterExperiments.experiment_sinus2()
    # ConverterExperiments.experiment_tri3()
    # ConverterExperiments.experiment_tri4()
    #ConverterExperiments.aliasing_experiment()
    # ConverterExperiments.test_exp()
    ConverterExperiments.filters_test()

    # ConverterExperiments.experiment_correlation()
    # ConverterExperiments.experiment_convolution()
