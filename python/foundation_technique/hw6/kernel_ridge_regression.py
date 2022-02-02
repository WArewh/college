import numpy as np

def rbf(x1, x2, gamma):
    n = len(x1)
    m = len(x2)
    K = np.zeros((n,m))
    for i in range(n):
        dis = np.linalg.norm(x1[i] - x2, axis=1)
        K[i] = np.exp(-gamma * dis)
    return K

class KernelRidgeRegression(object):
    def __init__(
        self,
        gamma: float,
        lmd: float,
        ) -> None:
        self._gamma = gamma
        self._lmd = lmd
        self._beta = None

    def fit(self, K, y):
        self._beta = np.linalg.inv(self._lmd * np.eye(len(K)) + K) @ y

    def compute_err(self, K, y):
        pred = np.sign(K.T.dot(self._beta))
        return np.mean(pred != y)
