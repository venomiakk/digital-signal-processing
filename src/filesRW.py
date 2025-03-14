import pickle
import os

class FileRW:
    @staticmethod
    def write_signal_to_file(sigObj, filename):
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
            
            # Write the signal object to file
            with open(filename, 'wb') as file:
                pickle.dump(sigObj, file)
            return True
        except Exception as e:
            print(f"Error saving signal to file: {e}")
            return False

    @staticmethod
    def read_signal_from_file(filename):
        try:
            # Check if file exists
            if not os.path.exists(filename):
                print(f"File not found: {filename}")
                return None
                
            # Read the signal object from file
            with open(filename, 'rb') as file:
                sigObj = pickle.load(file)
            return sigObj
        except Exception as e:
            print(f"Error reading signal from file: {e}")
            return None
        
if __name__ == "__main__":
    
    # from signals import SignalGenerator, SignalObject
    # from plots import plot_signal
    # s1 = SignalGenerator.sin_signal()
    # FileRW.write_signal_to_file(s1, "signal1.pkl")
    # s2 = FileRW.read_signal_from_file("signal1.pkl")
    # plot_signal(s2.signal, s2.time)
    
    print("FileRW")
