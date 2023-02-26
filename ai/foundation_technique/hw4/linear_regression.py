from cgi import test
from tkinter import W
import numpy as np

class LinearRegression(object):
    def __init__(
        self,
        lmd: float,
        ) -> None:
        """
        正则线性回归与验证

        参数:
            lmd (float): 正则化参数
        """
        self._lmd = lmd

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray
        ) -> tuple((np.ndarray,float)):
        w = np.linalg.inv(X.T @ X + self._lmd * np.eye(X.shape[1])) @ X.T @ y
        err = self.test(w, X, y)
        return w, err

    def test(
        self,
        w: np.ndarray,
        X: np.ndarray,
        y: np.ndarray
        ) -> float:
        """
        使用0/1错误
        """
        pred = np.sign(X @ w)
        return np.sum(pred != y) / X.shape[0]

    def simple_val(
        self,
        X: np.ndarray,
        y: np.ndarray,
        ratio: float):
        """
        简单交叉验证
        参数:
            ratio (float):训练资料占比
        """
        split = int(ratio*X.shape[0])
        X_train = X[:split]
        y_train = y[:split]
        X_val = X[split:]
        y_val = y[split:]

        w, train_err = self.train(X_train, y_train)
        val_err = self.test(w, X_val, y_val)

        return train_err, val_err

    def cross_val(
        self,
        X: np.ndarray,
        y: np.ndarray,
        k: int):
        """
        K折交叉验证
        """
        err = 0.0
        split = int(X.shape[0] / k)

        for i in range(k):
            start = i * split
            end = (i + 1) * split
            X_train = np.concatenate((X[:start], X[end:]))
            y_train = np.concatenate((y[:start], y[end:]))
            X_val = X[start:end]
            y_val = y[start:end]

            w, e = self.train(X_train, y_train)
            err += self.test(w, X_val, y_val)

        return err/k
