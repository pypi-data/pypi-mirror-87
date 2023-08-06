
class PublicKey:
    # public_key_id = -2 if mult_key
    # public_key_id = -1 if conj_key
    # public_key_id =  0 if  enc_key
    # public_key_id >= 1 if  rot_key 
    def __init__(self, public_key_id):
        self._public_key_id = public_key_id
        pass

    def get_public_key_id(self):
        return self._public_key_id

class SecretKey:
    def __init__(self, context):
        self._context = context
        pass

class PublicKeyPack:
    def __init__(self, context, secret_key):
        self._context = context
        pass
    
    def get_enc_key(self):
        enc_key = PublicKey(0)
        return enc_key

    def get_mult_key(self):
        mult_key = PublicKey(-2)
        return mult_key
    
    def get_left_rot_key(self, idx):
        half_degree = self._context._get_degree() // 2
        while idx < 0:
            idx += half_degree
        idx %= half_degree

        rotation_key = PublicKey(idx)
        return rotation_key

    def get_right_rot_key(self, idx):
        half_degree = self._context._get_degree() // 2
        tmp = (self._context._get_degree() // 2) - idx
        while tmp < 0:
            tmp += half_degree
        tmp %= half_degree
        
        rotation_key = PublicKey(tmp)
        return rotation_key

    def get_degree(self):
        return self._context.get_degree()

def generate_keys():
    log_degree = 17
    log_slots = 16
    degree = 2 ** log_degree

    modulus_bits = 1540
    quantize_bits = 51
    sp_num = 3

    from heaan.parameters import Parameters
    from heaan.context import Context

    params = Parameters()
    context = Context(params)
    context.make_bootstrappable(log_slots)
    secretkey = SecretKey(context)
    keypack = PublicKeyPack(context, secretkey)
    
    return (context, keypack, secretkey)