import numpy as np
class MLUtils():
    """
    Home of many different utility functions.
    """
    def __init__(self):
        self.data = None

    def xysplit(self, data=None):
        """
        This function splits data into x and y.
        :param data: Data to split into x and y.
        :return x, y: Returns x and y split data.
        """
        x=[]
        y=[]
        if data is not None:
            self.data = data
            i = 0
            for d in data:
                i+=1
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

        x=np.asarray(x, dtype=object)
        y=np.asarray(y, dtype=object)
        return x, y