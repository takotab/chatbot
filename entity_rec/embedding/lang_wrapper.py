import numpy as np

class language:
    
    def __init__(self,lang = "NL"):
        if lang == "NL":
            from .lang import NL

            self.emb_array = NL.EMB_ARRAY
            self.int2str = NL.INT2STR
            self.str2int = NL.STR2INT
        else:
            print("NOT YET SUPPORTED")
    
    def str2emb(self, word):

        if not word in self.str2int:
            if word.lower() in self.str2int:
                word = word.lower()
            else:
                return np.zeros(self.emb_array.shape)

        _int = self.str2int[word]
        return self.emb_array[_int, :]
    