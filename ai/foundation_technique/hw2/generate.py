import numpy as np 

def generate_data(
    range: tuple((int,int)),
    size: int,
    noise: float
    )-> tuple((np.ndarray,np.ndarray)):
    """
    产生带有噪音的均匀分布数据，针对第17、18题

    参数:
        range (tuple((int,int))): 范围
        size (int): 个数
        noise (float): 噪音比例
    """
    (low,high) = range
    X = np.random.uniform(low, high, size)
    y = np.sign(X) * np.where(np.random.random(size) < noise, low, high)

    return (X, y)
