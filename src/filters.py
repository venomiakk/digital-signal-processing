import numpy as np

class CustomSignalFilters:
    @staticmethod
    def convolve(h, x):
        n_len = len(x)
        m_len = len(h)
        y = np.zeros(n_len + m_len - 1)

        for n in range(n_len + m_len - 1):
            for k in range(m_len):
                if n - k >= 0 and n - k < n_len:
                    y[n] += h[k] * x[n - k]

        return y
    


if __name__ == "__main__":
    # Example usage
    h = np.array([1, 2, 3])
    x = np.array([4, 5, 6])
    result = CustomSignalFilters.convolve(h, x)
    print("Convolution Result:", result)