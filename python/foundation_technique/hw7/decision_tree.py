import numpy as np

def decision_stump(
        X: np.ndarray,
        y: np.ndarray,
        thetas: np.ndarray
    ) -> None:
        """
        决策桩实现

        返回值:
            本树决策参数(idx, theta)、子树的决策范围(range)
        """
        min_impurity = 1.0
        best_theta = 0
        idx = 0
        dim = X.shape[1]
        y = y.reshape((-1, 1))
        left_range, right_range = np.array([]), np.array([])

        for theta in thetas:
            impurity_all = []
            for i in range(dim):
                left_y = y[X[:, i] < theta[i]]
                right_y = y[X[:, i] >= theta[i]]
                impurity_left = compute_impurity(left_y) * left_y.size / y.size
                impurity_right = compute_impurity(right_y) * right_y.size / y.size
                impurity_all.append(impurity_left + impurity_right)
            
            i = np.argmin(impurity_all)
            impurity = impurity_all[i]

            if min_impurity > impurity:
                min_impurity = impurity
                idx = i
                best_theta = theta[idx]
                left_range = np.where(X[:,idx] < best_theta)[0]
                right_range = np.where(X[:,idx] > best_theta)[0]

        return (idx, best_theta), left_range, right_range

def compute_impurity(y):
    if y.shape[0] == 0: return np.array([0])
    pos = np.mean(y == 1, axis=0)
    neg = 1 - pos
    return 1 - pos * pos - neg * neg

class DecisionTree(object):
    """
    CART决策树
    
    参数:
        prune (bool): 是否修剪
        decision (tuple(int, int, float)): 决策桩得到的idx, theta
    """
    def __init__(self, prune=False, decision=None) -> None:
        self.prune = prune
        self.decision = decision
        self.left = None
        self.right = None

    def build(self, X, y):
        if compute_impurity(y) == 0: # 剩余全为一类
            return DecisionTree(decision=(-1, y[0]))

        fix_theta = np.sort(X, axis=0)
        fix_theta = (fix_theta[:-1] + fix_theta[1:]) / 2
        fix_theta = np.r_[fix_theta, fix_theta[-1].reshape(1, -1) * 1.1]

        decision, left_range, right_range = decision_stump(X, y, fix_theta)

        self.decision = decision

        if self.prune:
            if left_range.size != 0:
                y_left = y[left_range]
                y_left_domin = 1 if np.sum(y_left == 1) > y_left.size / 2 else -1   
                self.left = DecisionTree(decision=(-1, y_left_domin))
            else:
                self.left = DecisionTree(decision=(-1, -1))

            if right_range.size != 0:
                y_right = y[right_range]
                y_right_domin = 1 if np.sum(y_right == 1) > y_right.size / 2 else -1   
                self.right = DecisionTree(decision=(-1, y_right_domin))
            else:
                self.right = DecisionTree(decision=(-1, 1))

        else:
            if left_range.size != 0:
                X_left, y_left = X[left_range], y[left_range]
                self.left = DecisionTree().build(X_left, y_left)
            else:
                self.left = DecisionTree(decision=(-1, -1))

            if right_range.size != 0:
                X_right, y_right = X[right_range], y[right_range]
                self.right = DecisionTree().build(X_right, y_right)
            else:
                self.right = DecisionTree(decision=(-1, 1))

        return self

    def count_internal_nodes(self):
        if self == None: return 0
        if self.left == None and self.right == None: return 0
        l = 0
        r = 0
        if self.left != None: 
            l = self.left.count_internal_nodes()
        if self.right != None: 
            r = self.right.count_internal_nodes()
        return 1 + l + r

    def predict(self, X):
        """
        单个X预测
        """
        idx, theta = self.decision
        if idx == -1:
            return theta
        else:
            res = np.sign(X[idx] - theta)
            if res == -1:
                return self.left.predict(X)
            else:
                return self.right.predict(X)

    def predict_all(self, X):
        """
        群体X预测
        """
        pred = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            pred[i] = self.predict(X[i])
        return pred

    def compute_err(self, X, y):
        y_hat = self.predict_all(X)
        return np.mean(y_hat != y)