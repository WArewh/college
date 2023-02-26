import numpy as np

from decision_tree import DecisionTree

def bagging(idx_arr,cnt):
    """
    获得抽样索引

    参数:
        idx_arr (int): 索引数组
        cnt (int): 抽样数量
    """
    return np.random.choice(idx_arr, size=cnt)

class RandomForest(object):
    """
    随机森林实现
    
    参数:
        prune (bool): 是否修剪
    """
    def __init__(
        self,
        prune: bool=False
        ) -> None:
        self.prune = prune
        self.forest:list[DecisionTree] = []

    def build(self, X, y, T:int, N:int):
        """
        参数:
            T (int): 树的个数
            N (int): 抽样数量
        """
        for i in range(T):
            idx = bagging(range(N),N)
            X_sample = X[idx]
            y_sample = y[idx]
            tree = DecisionTree(self.prune)
            tree.build(X_sample, y_sample)
            self.forest.append(tree)

    def compute_forest_err(self, X, y, T):
        """
        计算前T个树的错误
        参数:
            prune (bool): 是否修剪
        """
        forest_pred = np.zeros(X.shape[0])
        for i in range(T):
            tree = self.forest[i]
            tree_pred = tree.predict_all(X)
            forest_pred += tree_pred
        
        forest_pred = np.sign(forest_pred)
        return np.mean(forest_pred != y)



    def compute_tree_err(self, X, y):
        e_ins = np.zeros(len(self.forest))
        
        for i in range(len(self.forest)):
            tree = self.forest[i]                
            e_in = tree.compute_err(X, y)
            e_ins[i] = e_in
        
        return e_ins
        
