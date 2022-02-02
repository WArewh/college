import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# def zero_one_err():
#     pass


class LogisticRegression(object):
    """
    实现逻辑回归

    参数:
        eta (float, optional): 学习率
        rand_grad (bool, optional): 是否随机梯度下降
    """
    
    def __init__(
        self,
        eta: float=0.001,
        rand_grad: bool=False,
        ) -> None:
        self._eta = eta
        self._rand_grad = rand_grad

    def _grad(
        self,
        w: np.ndarray,
        X: np.ndarray,
        y: np.ndarray):
        
        (size, dim) = X.shape
        sig = sigmoid(-y * X @ w)
        grad = 1 / size * np.sum(sig * -y * X, axis=0).reshape((dim, 1))
        return grad

    def train(self, X, y, max_iter: int) -> np.ndarray:
        w = np.zeros((X.shape[1], 1))

        if self._rand_grad:
            j = 0
            (size, dim) = X.shape
            for i in range(max_iter):
                w = w - self._eta * self._grad(w, X[j].reshape(1,dim), y[j])
                j += 1
                if j % size == 0:
                    j = 0
        else:         
            for i in range(max_iter):
                w = w - self._eta * self._grad(w, X, y)

        return w

    def test(
        self,
        w: np.ndarray,
        X: np.ndarray,
        y: np.ndarray
        ) -> float:
        """
        按题目使用0/1错误
        """
        pred = X @ w
        pred = np.sign(pred)
        
        return np.sum(pred != y)/X.shape[0]
