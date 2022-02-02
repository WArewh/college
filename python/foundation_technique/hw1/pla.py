import sys

import numpy as np


class PLA(object):
    """
    属性:
        eta (float, optional): 学习率
        rand (bool, optional): True随机访问，False顺序访问
        pock (bool, optional): True使用pocket，False不使用pocket
        max_iter: (int, optional): 最大迭代次数
    """

    def __init__(
            self,
            eta: float=1.0,
            rand: bool=False,
            pock: bool=False,
            max_iter: int=100
        ) -> None:

        self._eta = eta
        self._rand = rand
        self._pock = pock
        self._max_iter = max_iter

    def _rand_data(
        self,
        X: np.ndarray,
        y: np.ndarray
        ) -> tuple((np.ndarray, np.ndarray)):
        
        tmp = np.c_[X,y]
        np.random.shuffle(tmp)
        
        X = tmp[:,:-1]
        y = tmp[:,-1].reshape((X.shape[0],1))

        return (X, y)


    def _pla(self,X,y) -> tuple((int, np.ndarray)):
        """
        pla实现
        
        返回值:
            迭代次数和权值
        """
        iter = 0
        (cnt,dim) = X.shape
        w = np.zeros((dim,1))

        max_iter = self._max_iter

        while iter < max_iter:
            flag = False
            
            for i in range(cnt):
                pred = (X[i]@w*y[i])[0]

                if pred <= 0:
                    iter += 1
                    w = w + self._eta*y[i]*X[i].reshape(dim,1)
                    flag = True

            if not flag:
                break

        return (iter, w)


    def _pocket(self,X,y) -> tuple((int, np.ndarray)):
        """
        pocket实现
        
        返回值:
            迭代次数和训练好的权值
        """
        iter = 0
        (cnt,dim) = X.shape
        w = np.zeros((dim,1))
        best_w = w
        best_err = 1.0
        max_iter = self._max_iter

        while iter < max_iter:
            flag = False

            for i in range(cnt):
                pred = (X[i]@w*y[i])[0]

                if pred <= 0:
                    iter += 1
                    w = w + self._eta*y[i]*X[i].reshape(dim,1)
                    
                    err = self.compute_err(w,X,y)
                    
                    if err < best_err:
                        best_w = w
                        best_err = err

                if iter >= max_iter:
                    break

            if not flag:
                break
        
        return (iter, best_w)

    def train(self,X,y) -> tuple((int, float)):
        if self._rand:
            X,y = self._rand_data(X,y)
        
        if self._pock:
            return self._pocket(X,y)
        else:
            return self._pla(X,y)

    def compute_err(self,w,X,y) -> float:
        pred = X @ w * y
        return np.mean(pred <= 0)

