
class Message:

    def __init__(self, *args):

        if len(args) == 0:
            self._data = list()

        elif len(args) == 1:
            if type(args[0]) == list:
                self._data = args[0][:]
            else:
                print("Invalid type of input..")
                raise TypeError

        else:
            print("Invaid number of inputs..")
            raise TypeError
    
    def __repr__(self):
        return self._data

    def __len__(self):
        return len(self._data)
