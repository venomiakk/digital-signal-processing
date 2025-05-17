import numpy as np

from src.filters import CustomSignalFilters


class Simulation:
    def __init__(self,signal,
                 sampling_freq=1000,         # [Hz]
                 signal_speed=100.0,         # [m/s] - abstrakcyjny ośrodek
                 object_speed=1.0,           # [m/s] - prędkość obiektu
                 buffer_duration=0.1,        # [s]
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
        delay_est = max_index * self.dt
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
