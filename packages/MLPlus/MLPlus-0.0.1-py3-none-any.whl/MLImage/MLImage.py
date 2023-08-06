from PIL import Image
import numpy as np

class MLImage():
    def __init__(self, image=None, imagematrix=None):
        """
        :param image: Image.
        :param imagematrix: Numpy array image.
        """
        self.image = image
        self.imagematrix = imagematrix

    def toarray(self):
        """
        :return Numpy array image:
        """
        if self.image!=None:
            return np.array(self.image)
        else:
            raise ValueError("Requires A input image.")

    def toimage(self):
        """
        :return image:
        """
        return Image.fromarray(self.imagematrix)

    def loadimagefile(path):
        return MLImage(image=Image.open(path))