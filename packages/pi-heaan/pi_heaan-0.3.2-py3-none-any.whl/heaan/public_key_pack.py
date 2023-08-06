
import os
from heaan import PublicKey, SecretKey

class PublicKeyPack:

    def __init__(self, *args):

        self._rot_key_idx = [
            1,     2,     3,     4,     5,     6,     7,     8,     16,    24,    32,
            40,    48,    56,    64,    96,    128,   160,   192,   224,   256,   512,
            768,   1024,  1280,  1536,  1792,  2048,  3072,  4096,  5120,  6144,  7168,
            8192,  16384, 24576, 32768, 40960, 49152, 57344, 61440, 63488, 64512, 64544,
            65024, 65280, 65408, 65472, 65504, 65505, 65520, 65528, 65532, 65534, 65535
        ]

        if len(args) == 0:
            pass
        
        elif len(args) == 1:
            self._context = args[0]
        
        elif len(args) == 3:
            self._context = args[0]
            secret_key = args[1]
            key_dir_path = args[2]

            self.set_key_dir_path(key_dir_path)
            self.gen_encryption_key(secret_key)
            self.gen_multiplication_key(secret_key)
            self.gen_conjugation_key(secret_key)
            self.gen_rotation_key(secret_key)
            pass

        else:
            print("Invaid number of inputs..")
            raise TypeError

    def gen_encryption_key(self, secret_key):
        enc_key = PublicKey()
        enc_key._public_key_id = 0
        enc_key.save(self._context, self._key_dir_path + "/PK/EncKey.bin")
        pass
    
    def gen_multiplication_key(self, secret_key):
        mult_key = PublicKey()
        mult_key._public_key_id = -1
        mult_key.save(self._context, self._key_dir_path + "/PK/MultKey.bin")
        pass

    def gen_conjugation_key(self, secret_key):
        conj_key = PublicKey()
        conj_key._public_key_id = -2
        conj_key.save(self._context, self._key_dir_path + "/PK/ConjKey.bin")
        pass

    def gen_rotation_key(self, secret_key):
        for idx in self._rot_key_idx:
            rot_key = PublicKey()
            rot_key._public_key_id = idx
            rot_key.save(self._context, self._key_dir_path + "/PK/RotKey" + str(idx) + ".bin")
        pass

    def load(self, key_dir_path):
        self.set_key_dir_path(key_dir_path)
        pass

    def get_enc_key(self):
        enc_key = PublicKey()
        path = self.get_key_dir_path() + "/PK/EncKey.bin"
        enc_key.load(self._context, path)
        return enc_key

    def get_mult_key(self):
        mult_key = PublicKey()
        path = self.get_key_dir_path() + "/PK/MultKey.bin"
        mult_key.load(self._context, path)
        return mult_key
    
    def get_conj_key(self):
        conj_key = PublicKey()
        path = self.get_key_dir_path() + "/PK/ConjKey.bin"
        conj_key.load(self._context, path)
        return conj_key

    def get_left_rot_key(self, idx):
        half_degree = self._context.get_degree() // 2
        while idx < 0:
            idx += half_degree
        idx %= half_degree

        rot_key = PublicKey()
        rot_key.load(self._context, self.get_key_dir_path() + "/PK/RotKey" + str(idx) + ".bin")
        return rot_key

    def get_right_rot_key(self, idx):
        half_degree = self._context.get_degree() // 2
        tmp = half_degree - idx
        while tmp < 0:
            tmp += half_degree
        tmp %= half_degree

        rot_key = PublicKey()
        rot_key.load(self._context, self.get_key_dir_path() + "/PK/RotKey" + str(tmp) + ".bin")
        return rot_key

    def set_key_dir_path(self, key_dir_path):
        os.makedirs(name=key_dir_path+"/PK/", mode=0o775, exist_ok=True)
        self._key_dir_path = key_dir_path
        pass

    def get_key_dir_path(self):
        return self._key_dir_path

    