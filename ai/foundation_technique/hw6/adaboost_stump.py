import numpy as np
from torch import fix

def adaboost(
    X: np.ndarray,
    y: np.ndarray,
    T: int):
    """
    adaboost实现

    参数:
        T (int): 次数
    返回值:
        thetas (np.ndarray): 模型阈值
        alphas (np.ndarray): 模型权重
        signs (np.ndarray): 模型方向
        e_ins (np.ndarray): 模型训练误差
        idxs (np.ndarray): 模型选择维度
        u_sums (np.ndarray): 样本权重
        eps (np.ndarray): 加权错误
    """
    thetas = np.zeros(T)
    alphas = np.zeros(T)
    signs = np.zeros(T)
    e_ins = np.zeros(T)
    idxs = np.zeros(T,dtype=np.int)
    u_sums = np.zeros(T)
    eps = np.zeros(T)

    fix_theta = np.sort(X, axis=0)
    fix_theta = (fix_theta[:-1] + fix_theta[1:])/2
    fix_theta = np.r_[fix_theta, fix_theta[-1].reshape(1, -1) * 1.1]
    u = np.ones((X.shape[0], 1))/X.shape[0]

    for i in range(T):
        u_sums[i] = np.sum(u)
        (thetas[i], signs[i], e_ins[i], u, alphas[i], idxs[i], eps[i]) = decision_stump(X, y, u, fix_theta)
    
    return thetas, alphas, signs, e_ins, idxs, u_sums, eps

def decision_stump(
    X: np.ndarray,
    y: np.ndarray,
    u: np.ndarray,
    thetas: np.ndarray
    ):
    """
    决策桩实现
    """
    sign = 1                                # 方向
    min_e_in = 1.0
    best_theta = 0
    u_sum = np.sum(u)
    idx = 0
    dim = X.shape[1]
    y = y.reshape((-1, 1))

    for theta in thetas:
        pos_pred = np.where(X > theta, 1, -1)
        neg_pred = np.where(X < theta, 1, -1)
    
        err_pos = np.sum((pos_pred != y) * u, axis=0)
        err_neg = np.sum((neg_pred != y) * u, axis=0)
        err_all = np.append(err_pos,err_neg)

        i = np.argmin(err_all)
        min_err = err_all[i]

        if min_e_in > min_err:
            min_e_in = min_err
            idx = i % dim
            sign = - np.sign(i - 1.5)
            best_theta = theta[idx]
    
    x = X[:, idx]
    pred = np.where(x > best_theta , sign * 1, sign * -1).reshape((-1,1))
    eps = np.sum((pred != y) * u) / u_sum
    t = np.sqrt((1 - eps) / eps)
    alpha = np.log(t)
    u = u * np.exp(-y * alpha * pred) # 优化u的求法 见技法11节
    return (best_theta, sign, min_e_in, u, alpha, idx, eps)

def predict(
    thetas: np.ndarray,
    signs: np.ndarray,
    idxs: np.ndarray,
    alphas: np.ndarray,
    X: np.ndarray,
    ):
    """
    计算G的误差

    参数:
        thetas (np.ndarray): 阈值
        signs (np.ndarray): 方向
        idxs (np.ndarray): 选择的X维度
        alphas (np.ndarray): 假设权重
    """

    X_choose = X[:, idxs]
    pred = signs * np.sign((X_choose - thetas))
    pred = np.sign(np.sum(pred * alphas, axis = 1))
    return pred

def compute_err(y_hat, y):
    return np.mean(y_hat!=y)