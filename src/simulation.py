import numpy as np
import matplotlib.pyplot as plt
import os  # Dodaj ten import na początku pliku

from filters import CustomSignalFilters

class Simulation:
    def __init__(self,signal,
                 sampling_freq=1000,         # [Hz]
                 signal_speed=100.0,         # [m/s] - abstrakcyjny ośrodek
                 object_speed=1.0,           # [m/s] - prędkość obiektu
                 buffer_duration=0.5,        # [s] - zwiększone z 0.1 na 0.5
                 f1=50, f2=120,              # składniki sygnału sondującego
                 report_interval=0.2         # [s]
                 ):
        # Stałe
        self.fp = sampling_freq
        self.dt = 1 / self.fp
        self.v_object = object_speed
        self.v_signal = signal_speed
        self.buffer_len = int(buffer_duration * self.fp)
        self.report_interval = int(report_interval * self.fp)

        # Sygnał sondujący
        t = np.arange(self.buffer_len) * self.dt
        self.probe_signal = signal

        # Stan symulacji
        self.distance = 10.0  # m, startowa odległość
        self.time_step = 0

    def generate_reflected_signal(self):
        # Oblicz opóźnienie sygnału
        delay = 2 * self.distance / self.v_signal
        delay_samples = int(delay / self.dt)

        reflected = np.zeros(self.buffer_len)
        if delay_samples < self.buffer_len:
            reflected[delay_samples:] = self.probe_signal[:self.buffer_len - delay_samples]
        return reflected

    def estimate_distance(self, reflected_signal):
        corr = CustomSignalFilters.correlation_via_convolution(reflected_signal, self.probe_signal)
        max_index = np.argmax(corr)
        
        # Zakładając, że corr ma długość 2*buffer_len-1
        zero_lag_index = len(corr) // 2
        delay_est = (max_index - zero_lag_index) * self.dt
        distance_est = (delay_est * self.v_signal) / 2
        
        # Zwracamy również korelację dla wizualizacji
        return distance_est, corr, max_index
    
    def step(self):
        # Zaktualizuj rzeczywistą pozycję obiektu
        self.distance += self.v_object * self.dt

        # Generuj odbity sygnał
        reflected = self.generate_reflected_signal()

        # Oszacuj odległość
        distance_est, corr, max_index = self.estimate_distance(reflected)

        # Raportuj co `report_interval`
        if self.time_step % self.report_interval == 0:
            print(f"[t = {self.time_step * self.dt:.3f}s] "
                  f"Rzeczywista odległość: {self.distance:.2f} m, "
                  f"Oszacowana: {distance_est:.2f} m")
            
            # Wizualizacja co raport_interval
            self.visualize_signals(reflected, corr, max_index)

        self.time_step += 1
    
    def visualize_signals(self, reflected, corr, max_index):
        """Wizualizacja sygnału oryginalnego, odbitego i korelacji."""
        # Utwórz katalog na wykresy jeśli nie istnieje
        plots_dir = "plots"
        os.makedirs(plots_dir, exist_ok=True)
        
        t = np.arange(self.buffer_len) * self.dt
        
        plt.figure(figsize=(15, 10))
        
        # Oryginalny sygnał
        plt.subplot(3, 1, 1)
        plt.plot(t, self.probe_signal)
        plt.title(f"Oryginalny sygnał sondujący (t = {self.time_step * self.dt:.3f}s)")
        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda")
        plt.grid(True)
        
        # Odbity sygnał
        plt.subplot(3, 1, 2)
        plt.plot(t, reflected)
        plt.title(f"Odbity sygnał (odległość = {self.distance:.2f} m)")
        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda")
        plt.grid(True)
        
        # Korelacja
        plt.subplot(3, 1, 3)
        t_corr = np.linspace(-self.buffer_len * self.dt, self.buffer_len * self.dt, len(corr))
        plt.plot(t_corr, corr)
        
        # Oznaczenie maksimum korelacji
        zero_lag_index = len(corr) // 2
        delay = (max_index - zero_lag_index) * self.dt
        
        # Oznaczenie punktu zerowego i maksimum
        plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        plt.scatter(delay, corr[max_index], color='red', s=100, 
                   label=f'Opóźnienie: {delay:.4f}s')
        
        plt.title(f"Korelacja sygnałów (opóźnienie = {delay:.4f}s)")
        plt.xlabel("Opóźnienie [s]")
        plt.ylabel("Korelacja")
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        
        # Zapisz wykres do pliku zamiast wyświetlać
        filename = os.path.join(plots_dir, f"simulation_t{self.time_step * self.dt:.3f}s.png")
        plt.savefig(filename)
        plt.close()  # Zamknij wykres, aby zwolnić pamięć
        
        print(f"Zapisano wizualizację do {filename}")

    def run(self, duration_sec=5):
        steps = int(duration_sec / self.dt)
        for _ in range(steps):
            self.step()

if __name__ == "__main__":
    # Przykładowe użycie
    fs = 1000  # Częstotliwość próbkowania
    buffer_duration = 0.5  # [s]
    buffer_len = int(buffer_duration * fs)
    
    # Sygnał o odpowiedniej długości
    t = np.arange(buffer_len) / fs
    f1 = 1
    f2 = 3
    signal = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
    
    sim = Simulation(signal, buffer_duration=buffer_duration)
    sim.run(duration_sec=5)