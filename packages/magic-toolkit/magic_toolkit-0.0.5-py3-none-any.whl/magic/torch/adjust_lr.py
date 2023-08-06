import numpy as np
from torch.optim import lr_scheduler

class CosineAnnealingLR(object):
    def __init__(self, T_warm=10, T_max=100, eta_max=1, eta_min=0.001):
        """
        lr = lr_init * factor, so this class is designed to adjust factor
        :param T_warm: num of epochs for warm start
        :param T_max: maximum of epoch
        :param eta_max: defaut 1
        :param eta_min: defaut 0.001
        """
        self.eta_min = eta_min
        self.eta_max = eta_max
        self.T_max = T_max
        self.T_warm = T_warm

    def __call__(self, epoch):
        if epoch < self.T_warm:
            return self.eta_min + (self.eta_max - self.eta_min) / self.T_warm * epoch  # epoch start from 0
        return self.eta_min + 0.5 * (self.eta_max - self.eta_min) * \
               (1 + np.cos((epoch - self.T_warm) / self.T_max * np.pi))

def cos_annealing_scheduler(optimizer, T_warm=10, T_max=100, eta_max=1, eta_min=0.001):
    lr_lambda = CosineAnnealingLR(T_warm, T_max, eta_max, eta_min)
    scheduler = lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_lambda)
    return scheduler
