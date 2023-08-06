
import pickle

class Ciphertext:

    def __init__(self, *args):
        self._context = None

        if len(args) == 0:
            self._data = list()
            self._number_of_slots = 0
            self._modulus_bits = 0
            self._quantize_bits = 0

        elif len(args) == 1:
            if type(args[0]) == type(Ciphertext()):
                ctxt = args[0]
                self._data = ctxt._data[:]
                self._number_of_slots = ctxt._number_of_slots
                self._modulus_bits = ctxt._modulus_bits
                self._quantize_bits = ctxt._quantize_bits
            else:
                print("Invalid type of input..")
                raise TypeError

        elif len(args) == 4:
            degree = args[0]
            self._data = [0 for i in range(degree)]
            self._number_of_slots = args[1]
            self._modulus_bits = args[2]
            self._quantize_bits = args[3]

        else:
            print("Invaid number of inputs..")
            raise TypeError
    
    def copy_params(self, ctxt):
        self._number_of_slots = ctxt._number_of_slots
        self._modulus_bits = ctxt._modulus_bits
        self._quantize_bits = ctxt._quantize_bits
        
    def get_number_of_slots(self):
        return self._number_of_slots
    
    def get_modulus_bits(self):
        return self._modulus_bits

    def get_min_modulus_bits(self):
        return (4 * self._quantize_bits) + 60

    def get_quantize_bits(self):
        return self._quantize_bits

    def get_level(self):
        return (self._modulus_bits - self._quantize_bits - 10) // self._quantize_bits

    def load(self, stream):
        tmp = Ciphertext()
        with open(stream, 'rb') as f:
            tmp = pickle.load(f)
        self.__init__(tmp)
        pass
    
    def save(self, stream):
        with open(stream, 'wb') as f:
            pickle.dump(self, f)
        pass