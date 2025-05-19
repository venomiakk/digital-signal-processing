import numpy as np

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
        return distance_est

    def step(self):
        # Zaktualizuj rzeczywistą pozycję obiektu
        self.distance += self.v_object * self.dt

        # Generuj odbity sygnał
        reflected = self.generate_reflected_signal()

        # Oszacuj odległość
        distance_est = self.estimate_distance(reflected)

        # Raportuj co `report_interval`
        if self.time_step % self.report_interval == 0:
            print(f"[t = {self.time_step * self.dt:.3f}s] "
                  f"Rzeczywista odległość: {self.distance:.2f} m, "
                  f"Oszacowana: {distance_est:.2f} m")

        self.time_step += 1

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
    f1 = 50
    f2 = 120
    signal = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
    
    sim = Simulation(signal, buffer_duration=buffer_duration)
    sim.run(duration_sec=5)