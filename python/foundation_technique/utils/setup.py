import numpy as np
import matplotlib.pyplot as plt

def setup() -> None:
    plt.ion()
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    np.set_printoptions(formatter={'float': '{: 0.6f}'.format})