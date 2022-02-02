import numpy as np

class KMeans(object):
    """
    K均值实现
    """
    def __init__(self,k) -> None:
        """
        参数:
            k (int): 分类数量
        """
        self.k = k

    def fit(self, X):
        k = self.k
        size = X.shape[0]
        dim = X.shape[1]
        new_centers = np.zeros((k, dim))
        centers = np.zeros((k, dim))
        dis = np.zeros((size, k))
        y = np.zeros(size, dtype=np.int)
        
        # 随机初始点很重要
        for i in range(k):
            center_idx = np.random.randint(low=0, high=size, size=1)[0]
            centers[i] = X[center_idx]

        while True:
            for i in range(k):
                dis[:, i] = np.sum((X - centers[i])**2, axis=1)

            y = np.argmin(dis, axis=1)

            for i in range(k):
                choose_x = X[y == i]

                if choose_x.size != 0:
                    new_centers[i] = np.mean(choose_x, axis=0)
                else:
                    new_centers[i] = centers[i]

            gap = np.sum((centers - new_centers)**2)

            centers = new_centers

            if  gap < 1e-6:
                break

        return centers, y


    def compute_err(self, centers, X, y):
        return np.mean(np.sum((X - centers[y])**2, axis=1))