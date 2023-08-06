import numpy as np

class Encryptor:

    def __init__(self, *args):

        if len(args) == 0:
            pass

        elif len(args) == 1:
            self._context = args[0]

        else:
            print("Invalid number of inputs..")
            raise TypeError

    def encrypt(self, message, enc_key, ciphertext):
        ciphertext._data = message._data[:]
        ciphertext._quantize_bits = self._context._params._quantize_bits
        ciphertext._modulus_bits = self._context._params._modulus_bits
        ciphertext._number_of_slots = len(message)

        _scale_factor = 2**ciphertext._quantize_bits
        N = self._context._params._degree
        num_slots = ciphertext._number_of_slots
        encode_error = self._gen_encode_err(_scale_factor, N, num_slots)

        var_key = self._context._params.key_dist_variance
        var_err = self._context._params.err_dist_variance
        P = self._context._params._sp_modulus_bits

        encrypt_error = self._gen_encrypt_err(_scale_factor, var_key, var_err, N, P, num_slots)
        ciphertext._data += encode_error + encrypt_error

        self._context._update_used_function('encrypt')
        pass

    def _gen_encode_err(self, _scale_factor, N, num_slots):
        var = N/(24 * (_scale_factor**2))
        encode_error = np.random.normal(0, np.sqrt(var), num_slots)
        return encode_error

    def _gen_encrypt_err(self, _scale_factor, var_key, var_err, N, P, num_slots):
        var_encrypt  = var_err * (2*N*var_key + 1)/P + (N*var_key +1)/12
        encrypt_error = np.random.normal(0, np.sqrt(var_encrypt *N / (2* _scale_factor**2)), num_slots)
        return encrypt_error