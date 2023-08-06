import numpy as np

class Decryptor:
    
    def __init__(self, *args):

        if len(args) == 0:
            pass

        elif len(args) == 1:
            self._context = args[0]

        else:
            print("Invalid number of inputs..")
            raise TypeError

    def decrypt(self, ciphertext, secret_key, message):
        message._data = ciphertext._data[:]
        message._data = np.floor(message._data * (2**30)) / (2**30)
        self._context._update_used_function('decrypt')
        pass