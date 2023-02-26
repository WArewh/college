import numpy as np

def get_label(arr: np.ndarray, target: int) -> np.ndarray:
    """
    获得正负类标签
    参数:
        arr (np.ndarray): 需要标注的数组
        target (int): 正类对应数值
    """
    return np.where(arr==target, 1, -1)

# def compute_error(X, y, model):
#     pass
#     pred = np.array(model.predict(X))
#     acc = np.sum(pred == y)/y.shape[0]
#     return 1-acc