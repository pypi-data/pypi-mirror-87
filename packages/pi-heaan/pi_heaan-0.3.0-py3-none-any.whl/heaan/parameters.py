
import math
import pickle

class Parameters:

    def __init__(self, *args):
        self._sigma = 3.2
        self._h = 64

        if len(args) == 0:
            self._modulus_bits = 0
            self._quantize_bits = 0
            self._degree = 0
            self._sp_num = 0
            self._sp_modulus_bits = 0
            self._log_degree = 0
            pass

        elif len(args) == 2:
            self._depth = args[0]
            self._quantize_bits = args[1]
            self._modulus_bits = (self._depth*self._quantize_bits) + (self._quantize_bits+10)
            self._sp_num = 3
            self._sp_modulus_bits = math.ceil(self._modulus_bits / self._sp_num)
            self._degree = self._find_degree_128()
            self._log_degree = math.log(self._degree, 2)

        elif len(args) == 3:
            self._modulus_bits = args[0]
            self._quantize_bits = args[1]
            self._sp_num = args[2]
            self._sp_modulus_bits = math.ceil(self._modulus_bits / self._sp_num)
            self._degree = self._find_degree_128()
            self._log_degree = math.log(self._degree, 2)

        elif len(args) == 4:
            self._modulus_bits = args[1]
            self._quantize_bits = args[2]
            self._sp_num = args[3]
            self._sp_modulus_bits = math.ceil(self._modulus_bits / self._sp_num)
            self._degree = args[0]
            if self._degree < self._find_degree_128():
                print("This parameter is not 128-bit secure..")
                raise TypeError
            self._log_degree = math.log(self._degree, 2)
        
        else:
            print("Invaid number of inputs..")
            raise TypeError
        
        num_slots = self._degree //2
        Q = self._modulus_bits
        self.key_dist_bound = 1         # secret key generator distribution.
        self.key_dist_variance = 64/num_slots
        self.err_dist_variance = 3.2**2
        self.gdd_dist_variance = Q**2 / 12 #2**16 /12

    def get_quantize_bits(self):
        return self._quantize_bits
    
    def get_modulus_bits(self):
        return self._modulus_bits
    
    def get_degree(self):
        return self._degree

    def get_log_degree(self):
        return self._log_degree
    
    def get_sp_modulus_bits(self):
        return self._sp_modulus_bits
    
    def get_sp_num(self):
        return self._sp_num

    def get_sigma(self):
        return self._sigma
    
    def get_hamming_weight(self):
        return self._h

    def _find_degree_128(self):
        switch = self._modulus_bits + self._sp_modulus_bits
        if switch < 25:
            return 65536
        elif switch < 51:
            return 2048
        elif switch < 102:
            return 4096
        elif switch < 203:
            return 16384
        elif switch < 412:
            return 32768
        elif switch < 828:
            return 65536
        else:
            return 65536
        
    def load(self, path):
        tmp = Parameters()
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        modulus_bits = tmp._modulus_bits
        quantize_bits = tmp._quantize_bits
        sp_num = tmp._sp_num
        self.__init__(modulus_bits, quantize_bits, sp_num)
        pass
    
    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        pass
