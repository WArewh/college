import numpy as np

def load_dat(path: str, y: bool=True, y_start: int=-1):
    """
    加载dat文件
    
    参数
        path (string): 本地路径
        y (bool,optional): 是否有标签，True有，False没有
        y_start (int, optional): y的那一列位置
    """
    data = np.loadtxt(path)

    if y:
        if y_start == -1:
            X = data[:,:-1]
            y = data[:,-1]
        else:
            X = np.concatenate((data[:, :y_start], data[:, y_start + 1: ]), axis=1)
            y = data[:, y_start]
    else:
        X = data
        y = None

    return X, y, X.shape

# def load_