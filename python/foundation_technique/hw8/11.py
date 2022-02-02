import os

import numpy as np

from k_nearest_neighbor import KNN
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_curve

setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw8/hw8_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw8/hw8_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train11.dat")
test_save = os.path.join(os.path.dirname(__file__), "test11.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

K = [1, 3, 5, 7, 9]
e_ins = np.zeros_like(K, dtype=np.float) 
e_outs = np.zeros_like(K, dtype=np.float)

for i in range(len(K)):
    clf = KNN(X_train, y_train, K[i])
    e_ins[i] = clf.compute_err(X_train, y_train)
    e_outs[i] = clf.compute_err(X_test, y_test)

# 12
plot_curve(K, e_ins, title="12题", xlabel="K", ylabel="训练集错误率")

# 14
plot_curve(K, e_outs, title="14题", xlabel="K", ylabel="测试集错误率")

input("Program paused. Press ENTER to continue")