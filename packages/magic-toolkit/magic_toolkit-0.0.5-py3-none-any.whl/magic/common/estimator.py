"""abstract class"""

class Estimator(object):

    def fit(self):
        """ train model """
        raise NotImplementedError

    def predict(self, *inputs):
        """ do inference to predict """
        raise NotImplementedError

    def eval(self):
        """ do inference to evaluate model performance """
        raise NotImplementedError

    def summary(self):
        """model summary"""

    def load(self):
        """ load pre-trained model """

    def save(self):
        """ save trained model to local """

