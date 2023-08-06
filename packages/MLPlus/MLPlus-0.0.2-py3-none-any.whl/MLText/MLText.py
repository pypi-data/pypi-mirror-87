import numpy as np

class MLText():
    def __init__(self, text, vocab=[]):
        """
        :param text: Takes text as input.
        :param vocab: Takes vocab as input.
        """
        self.text = text
        if vocab != []:
            self.vocab = vocab
        else:
            self.vocab = []

    def onehotencode(self, spliter = "\n"):
        """
        :param spliter: What to split text by.
        :return onehotencoded: Return one hot encoded text.
        """
        if isinstance(self.text, str):
            if self.vocab == []:
                vocab = list(set(list(self.text)))
                self.vocab = vocab
            else:
                vocab = self.vocab
            list_text = list(map(list, self.text.split(spliter)))
            onehotencoded = []
            for line in list_text:
                onehotlist = []
                for i in line:
                    zeros = np.zeros(len(vocab))
                    zeros[vocab.index(i)] = 1
                    onehotlist.append(zeros)
                onehotencoded.append(np.asarray(onehotlist))
            onehotencoded = np.asarray(onehotencoded, dtype=object)
            return onehotencoded
        else:
            raise ValueError("Onehotencode only takes a string.")

    def onehotdecode(self, encodedvalue, seperator="\n"):
        """
        :param encodedvalue: The one hot encoded value.
        :param seperator: What you want to separate by when outputting.
        :return text: Returns decoded text.
        """
        text = ""
        for val in encodedvalue:
            for i in val:
                index = np.where(i==1)[0][0]
                text = text + self.vocab[index]
            text = text + seperator
        return text

    def loadtextfiles(path):
        f = open(path, "r")
        return MLText(f.read())