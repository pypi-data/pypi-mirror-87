
import pickle

class PublicKey:

    def __init__(self, *args):

        if len(args) == 0:
            self._number_of_prime = 0
            self._public_key_id = 0

        elif len(args) == 1:
            if type(args[0]) == type(PublicKey()):
                public_key = args[0]
                self._number_of_prime = public_key._number_of_prime
                self._public_key_id = public_key._public_key_id
            else:
                print("Invalid type of input..")
                raise TypeError

        else:
            print("Invaid number of inputs..")
            raise TypeError

    def get_public_key_id(self):
        return self._public_key_id
    
    def get_number_of_prime(self):
        return self._number_of_prime
    
    def load(self, *args):

        if len(args) == 1:
            path = args[0]

        elif len(args) == 2:
            context = args[0]
            path = args[1]

        else:
            print("Invalid number of inputs..")
            raise TypeError
        
        tmp = PublicKey()
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        self.__init__(tmp)
        pass
    
    def save(self, *args):

        if len(args) == 1:
            path = args[0]

        elif len(args) == 2:
            context = args[0]
            path = args[1]
            context.save_params(path)
            
        else:
            print("Invalid number of inputs..")
            raise TypeError
        
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        pass