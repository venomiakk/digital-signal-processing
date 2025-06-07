from transformations import Transfomations
import numpy as np
import time
import csv
from plots import plot_W1, plot_W2, plot_raw_signal
import os

def time_experiment(tofile=False):
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    
    results = []
    results.append(("f","S1", "S2", "S3"))
    
    dft_results = ["DFT"]
    # DFT
    star_time = time.perf_counter()
    X1 = Transfomations.dft(s1)
    end_time = time.perf_counter()
    print(f"S1 DFT time: {end_time - star_time:.6f} seconds")
    dft_results.append(f"{end_time - star_time:.6f}")

    star_time = time.perf_counter()
    X2 = Transfomations.dft(s2)
    end_time = time.perf_counter()
    print(f"S2 DFT time: {end_time - star_time:.6f} seconds")
    dft_results.append(f"{end_time - star_time:.6f}")

    star_time = time.perf_counter()
    X3 = Transfomations.dft(s3)
    end_time = time.perf_counter()
    print(f"S3 DFT time: {end_time - star_time:.6f} seconds")
    dft_results.append(f"{end_time - star_time:.6f}")
    results.append(dft_results)

    # FFT
    fft_results = ["FFTDIT"]
    star_time = time.perf_counter()
    X1_fft = Transfomations.fft_dit(s1)
    end_time = time.perf_counter()
    print(f"S1 FFT DIT time: {end_time - star_time:.6f} seconds")
    fft_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X2_fft = Transfomations.fft_dit(s2)
    end_time = time.perf_counter()
    print(f"S2 FFT DIT time: {end_time - star_time:.6f} seconds")
    fft_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X3_fft = Transfomations.fft_dit(s3)
    end_time = time.perf_counter()
    print(f"S3 FFT DIT time: {end_time - star_time:.6f} seconds")
    fft_results.append(f"{end_time - star_time:.6f}")
    results.append(fft_results)

    # DCT
    dct_results = ["DCT"]
    star_time = time.perf_counter()
    X1_dct = Transfomations.dct(s1)
    end_time = time.perf_counter()
    print(f"S1 DCT time: {end_time - star_time:.6f} seconds")
    dct_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X2_dct = Transfomations.dct(s2)
    end_time = time.perf_counter()
    print(f"S2 DCT time: {end_time - star_time:.6f} seconds")
    dct_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X3_dct = Transfomations.dct(s3)
    end_time = time.perf_counter()
    print(f"S3 DCT time: {end_time - star_time:.6f} seconds")
    dct_results.append(f"{end_time - star_time:.6f}")
    results.append(dct_results)

    # FCT
    fct_results = ["FCT"]
    star_time = time.perf_counter()
    X1_fct = Transfomations.fct(s1)
    end_time = time.perf_counter()
    print(f"S1 FCT time: {end_time - star_time:.6f} seconds")
    fct_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X2_fct = Transfomations.fct(s2)
    end_time = time.perf_counter()
    print(f"S2 FCT time: {end_time - star_time:.6f} seconds")
    fct_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X3_fct = Transfomations.fct(s3)
    end_time = time.perf_counter()
    print(f"S3 FCT time: {end_time - star_time:.6f} seconds")
    fct_results.append(f"{end_time - star_time:.6f}")
    results.append(fct_results)

    # WHT
    wht_results = ["WHT"]
    star_time = time.perf_counter()
    X1_wht = Transfomations.wht(s1)
    end_time = time.perf_counter()
    print(f"S1 WHT time: {end_time - star_time:.6f} seconds")
    wht_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X2_wht = Transfomations.wht(s2)
    end_time = time.perf_counter()
    print(f"S2 WHT time: {end_time - star_time:.6f} seconds")
    wht_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X3_wht = Transfomations.wht(s3)
    end_time = time.perf_counter()
    print(f"S3 WHT time: {end_time - star_time:.6f} seconds")
    wht_results.append(f"{end_time - star_time:.6f}")
    results.append(wht_results)

    # FWHT
    fwht_results = ["FWHT"]
    star_time = time.perf_counter()
    X1_fwht = Transfomations.fwht(s1)
    end_time = time.perf_counter()
    print(f"S1 FWHT time: {end_time - star_time:.6f} seconds")
    fwht_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X2_fwht = Transfomations.fwht(s2)
    end_time = time.perf_counter()
    print(f"S2 FWHT time: {end_time - star_time:.6f} seconds")
    fwht_results.append(f"{end_time - star_time:.6f}")
    star_time = time.perf_counter()
    X3_fwht = Transfomations.fwht(s3)
    end_time = time.perf_counter()
    print(f"S3 FWHT time: {end_time - star_time:.6f} seconds")
    fwht_results.append(f"{end_time - star_time:.6f}")
    results.append(fwht_results)

    if tofile:
        with open("results.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(results)

def plot_raw_signals(tofile=False):
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    if tofile==False:
        plot_raw_signal(s1, t, tofile=True, title="S1")
        plot_raw_signal(s2, t, tofile=True, title="S2")
        plot_raw_signal(s3, t, tofile=True, title="S3")
    else:
        os.makedirs("plots", exist_ok=True)
        fig1 = plot_raw_signal(s1,toplot=False, title="S1")
        fig1.savefig("plots/S1_raw_signal.png")
        fig2 = plot_raw_signal(s2, toplot=False, title="S2")
        fig2.savefig("plots/S2_raw_signal.png")
        fig3 = plot_raw_signal(s3, toplot=False, title="S3")
        fig3.savefig("plots/S3_raw_signal.png")

def dft_plots(tofile=False):
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    
    X1 = Transfomations.dft(s1)
    X2 = Transfomations.dft(s2)
    X3 = Transfomations.dft(s3)
    
    if tofile==False:
        plot_W1(X1, title="S1 DFT")
        plot_W2(X1, title="S1 DFT")
        plot_W1(X2, title="S2 DFT")
        plot_W2(X2, title="S2 DFT")
        plot_W1(X3, title="S3 DFT")
        plot_W2(X3, title="S3 DFT")
    else:
        os.makedirs("plots/dft", exist_ok=True)
        fig1 = plot_W1(X1, title="S1 DFT", tofile=False)
        fig1.savefig("plots/dft/S1_DFT_w1.png")
        fig2 = plot_W2(X1, title="S1 DFT", tofile=False)
        fig2.savefig("plots/dft/S1_DFT_w2.png")
        fig3 = plot_W1(X2, title="S2 DFT", tofile=False)
        fig3.savefig("plots/dft/S2_DFT_w1.png")
        fig4 = plot_W2(X2, title="S2 DFT", tofile=False)
        fig4.savefig("plots/dft/S2_DFT_w2.png")
        fig5 = plot_W1(X3, title="S3 DFT", tofile=False)
        fig5.savefig("plots/dft/S3_DFT_w1.png")
        fig6 = plot_W2(X3, title="S3 DFT", tofile=False)
        fig6.savefig("plots/dft/S3_DFT_w2.png")
        fig7 = plot_raw_signal(X1, toplot=False, title="S1 DFT")
        fig7.savefig("plots/dft/S1_DFT_raw.png")
        fig8 = plot_raw_signal(X2, toplot=False, title="S2 DFT")
        fig8.savefig("plots/dft/S2_DFT_raw.png")
        fig9 = plot_raw_signal(X3, toplot=False, title="S3 DFT")
        fig9.savefig("plots/dft/S3_DFT_raw.png")

def fft_plots(tofile=False):
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    
    X1_fft = Transfomations.fft_dit(s1)
    X2_fft = Transfomations.fft_dit(s2)
    X3_fft = Transfomations.fft_dit(s3)

    if tofile==False:
        plot_W1(X1_fft, title="S1 FFT DIT")
        plot_W2(X1_fft, title="S1 FFT DIT")
        plot_W1(X2_fft, title="S2 FFT DIT")
        plot_W2(X2_fft, title="S2 FFT DIT")
        plot_W1(X3_fft, title="S3 FFT DIT")
        plot_W2(X3_fft, title="S3 FFT DIT")
    else:
        os.makedirs("plots/fft", exist_ok=True)
        fig1 = plot_W1(X1_fft, title="S1 FFT DIT", tofile=False)
        fig1.savefig("plots/fft/S1_FFT_DIT_w1.png")
        fig2 = plot_W2(X1_fft, title="S1 FFT DIT", tofile=False)
        fig2.savefig("plots/fft/S1_FFT_DIT_w2.png")
        fig3 = plot_W1(X2_fft, title="S2 FFT DIT", tofile=False)
        fig3.savefig("plots/fft/S2_FFT_DIT_w1.png")
        fig4 = plot_W2(X2_fft, title="S2 FFT DIT", tofile=False)
        fig4.savefig("plots/fft/S2_FFT_DIT_w2.png")
        fig5 = plot_W1(X3_fft, title="S3 FFT DIT", tofile=False)
        fig5.savefig("plots/fft/S3_FFT_DIT_w1.png")
        fig6 = plot_W2(X3_fft, title="S3 FFT DIT", tofile=False)
        fig6.savefig("plots/fft/S3_FFT_DIT_w2.png")
        fig7 = plot_raw_signal(X1_fft, toplot=False, title="S1 FFT DIT")
        fig7.savefig("plots/fft/S1_FFT_DIT_raw.png")
        fig8 = plot_raw_signal(X2_fft, toplot=False, title="S2 FFT DIT")
        fig8.savefig("plots/fft/S2_FFT_DIT_raw.png")
        fig9 = plot_raw_signal(X3_fft, toplot=False, title="S3 FFT DIT")
        fig9.savefig("plots/fft/S3_FFT_DIT_raw.png")

def dct_plots(tofile=False):
    
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    
    X1_dct = Transfomations.dct(s1)
    X2_dct = Transfomations.dct(s2)
    X3_dct = Transfomations.dct(s3)

    if tofile==False:
        plot_raw_signal(X1_dct, toplot=False, title="S1 DCT")
        plot_raw_signal(X2_dct, toplot=False, title="S2 DCT")
        plot_raw_signal(X3_dct, toplot=False, title="S3 DCT")
    else:
        os.makedirs("plots/dct", exist_ok=True)
        fig1 = plot_raw_signal(X1_dct, toplot=False, title="S1 DCT")
        fig1.savefig("plots/dct/S1_DCT.png")
        fig2 = plot_raw_signal(X2_dct, toplot=False, title="S2 DCT")
        fig2.savefig("plots/dct/S2_DCT.png")
        fig3 = plot_raw_signal(X3_dct, toplot=False, title="S3 DCT")
        fig3.savefig("plots/dct/S3_DCT.png")

def fct_plots(tofile=False):
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    
    X1_fct = Transfomations.fct(s1)
    X2_fct = Transfomations.fct(s2)
    X3_fct = Transfomations.fct(s3)

    if tofile==False:
        plot_raw_signal(X1_fct, toplot=False, title="S1 FCT")
        plot_raw_signal(X2_fct, toplot=False, title="S2 FCT")
        plot_raw_signal(X3_fct, toplot=False, title="S3 FCT")
    else:
        os.makedirs("plots/fct", exist_ok=True)
        fig1 = plot_raw_signal(X1_fct, toplot=False, title="S1 FCT")
        fig1.savefig("plots/fct/S1_FCT.png")
        fig2 = plot_raw_signal(X2_fct, toplot=False, title="S2 FCT")
        fig2.savefig("plots/fct/S2_FCT.png")
        fig3 = plot_raw_signal(X3_fct, toplot=False, title="S3 FCT")
        fig3.savefig("plots/fct/S3_FCT.png")

def wht_plots(tofile=False):
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    
    X1_wht = Transfomations.wht(s1)
    X2_wht = Transfomations.wht(s2)
    X3_wht = Transfomations.wht(s3)

    if tofile==False:
        plot_raw_signal(X1_wht, toplot=False, title="S1 WHT")
        plot_raw_signal(X2_wht, toplot=False, title="S2 WHT")
        plot_raw_signal(X3_wht, toplot=False, title="S3 WHT")
    else:
        os.makedirs("plots/wht", exist_ok=True)
        fig1 = plot_raw_signal(X1_wht, toplot=False, title="S1 WHT")
        fig1.savefig("plots/wht/S1_WHT.png")
        fig2 = plot_raw_signal(X2_wht, toplot=False, title="S2 WHT")
        fig2.savefig("plots/wht/S2_WHT.png")
        fig3 = plot_raw_signal(X3_wht, toplot=False, title="S3 WHT")
        fig3.savefig("plots/wht/S3_WHT.png")
    
def fwht_plots(tofile=False):
    s1, s2, s3 = Transfomations.generate_signals()
    f_pr = 16  # Hz
    T = 1 / f_pr
    N = 64  # liczba próbek 
    t = np.arange(N) * T
    
    X1_fwht = Transfomations.fwht(s1)
    X2_fwht = Transfomations.fwht(s2)
    X3_fwht = Transfomations.fwht(s3)

    if tofile==False:
        plot_raw_signal(X1_fwht, toplot=False, title="S1 FWHT")
        plot_raw_signal(X2_fwht, toplot=False, title="S2 FWHT")
        plot_raw_signal(X3_fwht, toplot=False, title="S3 FWHT")
    else:
        os.makedirs("plots/fwht", exist_ok=True)
        fig1 = plot_raw_signal(X1_fwht, toplot=False, title="S1 FWHT")
        fig1.savefig("plots/fwht/S1_FWHT.png")
        fig2 = plot_raw_signal(X2_fwht, toplot=False, title="S2 FWHT")
        fig2.savefig("plots/fwht/S2_FWHT.png")
        fig3 = plot_raw_signal(X3_fwht, toplot=False, title="S3 FWHT")
        fig3.savefig("plots/fwht/S3_FWHT.png")

if __name__ == "__main__":
    time_experiment()
    # time_experiment(tofile=True)
    # plot_raw_signals(tofile=True)
    # dft_plots(tofile=True)
    # fft_plots(tofile=True)
    # dct_plots(tofile=True)
    # fct_plots(tofile=True)
    # wht_plots(tofile=True)
    # fwht_plots(tofile=True)
