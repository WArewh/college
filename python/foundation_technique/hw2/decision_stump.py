import numpy as np 

def decision_stump(X: np.ndarray, y: np.ndarray) -> tuple((np.ndarray, int, float)):
    """
    决策桩实现
    
    返回值:
        阈值、方向、样本误差
    """
    
    size = X.shape[0]
    sign = 1                                    # 方向
    min_e_in = size
    best_theta = 0


    sorted_X = np.sort(X)
    thetas = (sorted_X[:-1:1] + sorted_X[1::1]) / 2
    
    thetas = np.append(thetas,sorted_X[-1] * 1.1)

    for theta in thetas:
        y_pos = np.where(X > theta, 1, -1)  # 正向
        y_neg = np.where(X < theta, 1, -1)  # 负向
        
        err_pos = np.sum(y_pos != y)/size
        err_neg = np.sum(y_neg != y)/size

        if err_pos < err_neg:
            if min_e_in > err_pos:
                sign = 1
                min_e_in = err_pos
                best_theta = theta
        else:
            if min_e_in > err_neg:
                sign = -1
                min_e_in = err_neg
                best_theta = theta

    return (best_theta, sign, min_e_in)

def compute_err(
    theta: np.ndarray,
    s:int,
    X: np.ndarray,
    y: np.ndarray):
    """
    参数:
        s (int): 方向
    """
    pred = s * np.sign(X - theta)
    return np.sum(pred != y) / X.shape[0]

