import numpy as np



class KNN(object):
    """
    K最近邻实现
    """
    def __init__(
        self,
        X,
        y,
        k: int
        ) -> None:
        """
        参数:
            X: 训练集数据
            y: 训练集标签
            k (int): 参考数量
        """
        self.X = X
        self.y = y
        self.k = k

    def predict(self, X):
        pred = np.zeros(X.shape[0])
        for i in range(len(X)):
            dis = np.linalg.norm(X[i] - self.X, axis=1)
            k_min_dis_i = np.argsort(dis)[: self.k]
            pred[i] = np.sign(np.sum(self.y[k_min_dis_i]))
        
        return pred

    def compute_err(self, X, y):
        pred = self.predict(X)
        return np.mean(pred != y)