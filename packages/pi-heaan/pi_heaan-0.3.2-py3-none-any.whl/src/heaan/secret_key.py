
import pickle

class SecretKey:

    def __init__(self, *args):

        if len(args) > 1:
            print("Invaid number of inputs..")
            raise TypeError

    def load(self, *args):

        if len(args) == 1:
            path = args[0]

        elif len(args) == 2:
            context = args[0]
            path = args[1]
            context.load_params(path)

        else:
            print("Invalid number of inputs..")
            raise TypeError
        
        tmp = SecretKey()
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