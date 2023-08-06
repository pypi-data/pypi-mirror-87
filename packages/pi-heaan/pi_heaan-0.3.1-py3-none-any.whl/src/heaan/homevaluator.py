
from heaan import Ciphertext, Message, PublicKey, PublicKeyPack, Encryptor
import numpy as np

class HomEvaluator:
    
    def __init__(self, *args):

        if len(args) == 0:
            pass

        elif len(args) == 1:
            self._context = args[0]

        else:
            print("Invalid number of inputs..")
            raise TypeError
    
    def gen_key_switch_error(self, context, num_slots):
        params = context._params
        d_l = params._sp_num
        P = params._sp_modulus_bits
        N = params._degree
        _scale_factor = 2**params._quantize_bits
        _variance = d_l * N * params.gdd_dist_variance * params.err_dist_variance / P + (N * params.key_dist_variance + 1 )/12
        error = np.random.normal(0, np.sqrt(_variance *N / (2* _scale_factor**2)), num_slots)
        return error
        
    def gen_rescale_error(self, context, num_slots):
        params = context._params
        N = params._degree
        _scale_factor = 2**params._quantize_bits
        _variance =(N * params.key_dist_variance +1)/12
        error = np.random.normal(0, np.sqrt(_variance *N / (2* _scale_factor**2)), num_slots)
        return error


    def negate(self, ctxt, ctxt_out):
        ctxt_out.copy_params(ctxt)
        ctxt_out._data = [-data for data in ctxt._data]

        num_slots = len(ctxt._data)
        relinearlization_error = self.gen_key_switch_error(self._context, num_slots)

        encode_error = Encryptor(self._context)._gen_encode_err(2**ctxt._quantize_bits, self._context._params._degree, num_slots)
        delta = 2**ctxt._quantize_bits
        ctxt_out._data += (encode_error+relinearlization_error)/delta

        self._context._update_used_function('negate')
        pass

    def add(self, input1, input2, output):
        input1_data = input1._data

        input2_type = type(input2)
        if input2_type in {int, float}:
            number_of_slots = input1.get_number_of_slots()
            input2_data = [input2] * number_of_slots
            output.copy_params(input1)
            pass
        else:
            self._check_number_of_slots(input1, input2)

            if input2_type == type(Message()):
                output.copy_params(input1)
            elif input2_type == type(Ciphertext()):
                if input1._modulus_bits > input2._modulus_bits:
                    output.copy_params(input2)
                else:
                    output.copy_params(input1)

            input2_data = input2._data
            pass
        
        output._data = [data1+data2 for data1,data2 in zip(input1_data, input2_data)]

        if input2_type in {int, float}:
            self._context._update_used_function('add_const')
        else:
            self._context._update_used_function('add')
        pass

    def sub(self, input1, input2, output):
        input1_data = input1._data

        input2_type = type(input2)
        if input2_type in {int, float}:
            number_of_slots = input1.get_number_of_slots()
            input2_data = [input2] * number_of_slots
            output.copy_params(input1)
            pass
        else:
            self._check_number_of_slots(input1, input2)

            if input2_type == type(Message()):
                output.copy_params(input1)
            elif input2_type == type(Ciphertext()):
                if input1._modulus_bits > input2._modulus_bits:
                    output.copy_params(input2)
                else:
                    output.copy_params(input1)

            input2_data = input2._data
            pass

        output._data = [data1-data2 for data1,data2 in zip(input1_data, input2_data)]

        if input2_type in {int, float}:
            self._context._update_used_function('sub_const')
        else:
            self._context._update_used_function('sub')
        pass

    def divide_by_pow_of_two(self, ctxt, bits_div, ctxt_out):
        ctxt_out.copy_params(ctxt)
        ctxt_out._data = [data/pow(2,bits_div) for data in ctxt._data]
        ctxt_out._modulus_bits -= bits_div

        self._context._update_used_function('div_pow2')
        pass

    def mult(self, *args):
        input1 = args[0]
        input2_type = type(args[1])
        
        quantize_bits = input1._quantize_bits

        num_slots = len(input1._data)
        relinearlization_error = self.gen_key_switch_error(self._context, num_slots)
        rescale_error = self.gen_rescale_error(self._context, num_slots)
        
        if len(args) == 3:
            input1 = args[0]
            input2 = args[1]
            output = args[2]

            encode_error = Encryptor(self._context)._gen_encode_err(2**input1._quantize_bits, self._context._params._degree, num_slots)

            self._mult_without_rescale(input1, input2, output)
            output._data+=encode_error
        elif len(args) == 4:
            input1 = args[0]
            input2 = args[1]
            mult_key = args[2]
            output = args[3]

            self._mult_without_rescale(input1, input2, mult_key, output)
            
        else:
            print("Invalid number of inputs..")
            raise TypeError
        
        delta = 2**input1._quantize_bits
        output._data += relinearlization_error/delta


        self._rescale_by(output, quantize_bits)
        if input2_type !=int:
            output._data +=+ rescale_error

        if input2_type == int:
            output._modulus_bits += quantize_bits
            self._context._update_used_function('mult_const_int')
        elif input2_type == float:
            self._context._update_used_function('mult_const_float')
        elif input2_type == type(Message()):
            self._context._update_used_function('mult_msg')
        elif input2_type == type(Ciphertext()):
            self._context._update_used_function('mult')
        pass

    def square(self, ctxt, mult_key, output):
        self.mult(ctxt, ctxt, mult_key, output)
        pass

    def left_rotate(self, *args):
        ctxt = args[0]
        rot_idx = args[1]
        ctxt_out = args[3]

        if type(args[2]) == type(PublicKey()):
            rot_key = args[2]
        elif type(args[2]) == type(PublicKeyPack()):
            rot_key = args[2].get_left_rot_key(rot_idx)
        else:
            print("Invalid type of input..")
            raise TypeError

        if (rot_key.get_public_key_id() != rot_idx):
            print("ID of input public key is not " + str(rot_idx))
            raise TypeError
        
        number_of_slots = ctxt._number_of_slots
        while rot_idx < 0:
            rot_idx += number_of_slots
        rot_idx %= number_of_slots

        ctxt_out.copy_params(ctxt)
        ctxt_out._data = np.array(list(ctxt._data[rot_idx:]) + list(ctxt._data[:rot_idx]))

        automorphism_error = self.gen_key_switch_error(self._context, number_of_slots)
        ctxt_out._data += automorphism_error

        self._context._update_used_function('rotate')
        pass

    def right_rotate(self, *args):
        ctxt = args[0]
        rot_idx = args[1]
        ctxt_out = args[3]

        if type(args[2]) == type(PublicKey()):
            rot_key = args[2]
        elif type(args[2]) == type(PublicKeyPack()):
            rot_key = args[2].get_right_rot_key(rot_idx)
        else:
            print("Invalid type of input..")
            raise TypeError

        number_of_slots = ctxt._number_of_slots
        left_rot_idx = number_of_slots - rot_idx
        
        self.left_rotate(ctxt, left_rot_idx, rot_key, ctxt_out)
        pass

    def bootstrap(self, ctxt, keypack, ctxt_out):
        ctxt_out.copy_params(ctxt)
        ctxt_out._data = ctxt._data
        ctxt_out._modulus_bits = 775
        num_slots = len(ctxt_out._data)
        bootstrap_err = np.random.normal(0, 2**(-33), num_slots)
        ctxt_out._data +=bootstrap_err
                
        self._context._update_used_function('bootstrap')
        pass

    def kill_imag(self, ctxt, keypack, ctxt_out):
        self._mod_down_by(ctxt, 1, ctxt_out)

        self._context._update_used_function('kill_imag')
        pass

    def _mult_without_rescale(self, *args):
        if len(args) == 3:
            input1 = args[0]
            input2 = args[1]
            output = args[2]

        elif len(args) == 4:
            input1 = args[0]
            input2 = args[1]
            output = args[3]

        else:
            print("Invalid number of inputs..")
            raise TypeError

        input1_data = input1._data

        input2_type = type(input2)
        if input2_type in {int, float}:
            number_of_slots = input1.get_number_of_slots()
            input2_data = [input2] * number_of_slots
            output.copy_params(input1)
            pass
        else:
            self._check_number_of_slots(input1, input2)

            if input2_type == type(Message()):
                output.copy_params(input1)
            elif input2_type == type(Ciphertext()):
                if input1._modulus_bits > input2._modulus_bits:
                    output.copy_params(input2)
                else:
                    output.copy_params(input1)

            input2_data = input2._data
            pass

        output._quantize_bits += input1._quantize_bits
        output._data = [data1*data2 for data1,data2 in zip(input1_data, input2_data)]
        pass

    def _mod_down_by(self, ctxt, bits_down, ctxt_out):
        ctxt_out.copy(ctxt)
        ctxt_out._modulus_bits -= bits_down
        pass

    def _rescale_by(self, ctxt, bits_down):
        ctxt._modulus_bits -= bits_down
        ctxt._quantize_bits -= bits_down
        pass

    def _check_number_of_slots(self, input1, input2):
        input1_number_of_slots = input1._number_of_slots

        input2_type = type(input2)
        if input2_type == type(Message()):
            input2_number_of_slots = len(input2)
        elif input2_type == type(Ciphertext()):
            input2_number_of_slots = input2._number_of_slots
        else:
            print("Invalid input type..")
            raise TypeError
        
        if input1_number_of_slots != input2_number_of_slots:
            print("Both inputs should have same number_of_slots..")
            raise ValueError

    def _check_quantize_bits(self, ctxt1, ctxt2):
        if ctxt1._quantize_bits != ctxt2._quantize_bits:
            print("Both ciphertexts should have same quantize_bits..")
            raise ValueError