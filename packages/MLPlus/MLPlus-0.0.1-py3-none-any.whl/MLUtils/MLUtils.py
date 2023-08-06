import numpy as np
class MLUtils():
    def __init__(self):
        self.data = None

    def xysplit(self, data=None):
        x=[]
        y=[]
        if data is not None:
            self.data = data
            i = 0
            for d in data:
                i+=1
                print(d)
                print(1)
                if i%2==1:
                    x.append(d)
                else:
                    y.append(d)
        elif self.data is not None:
            i = 0
            for d in data:
                i += 1
                if i % 2 == 1:
                    x.append(d)
                else:
                    y.append(d)
        else:
            raise ValueError("Requires input.")

        x=np.asarray(x)
        y=np.asarray(y)
        return x, y