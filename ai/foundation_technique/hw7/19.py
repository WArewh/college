import os

import numpy as np

from random_forest import RandomForest
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_curve


setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw7/hw7_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw7/hw7_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train.dat")
test_save = os.path.join(os.path.dirname(__file__), "test.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

# coursera 19-20题 100->10 结果差不多
# T = 300
# iter = 10
# aver_forest_e_in = 0.0
# aver_forest_e_out = 0.0

# for i in range(iter):
#     rf = RandomForest(prune=True)
#     rf.build(X_train, y_train, T, train_cnt)
#     aver_forest_e_in += rf.compute_forest_err(X_train, y_train, T)
#     aver_forest_e_out += rf.compute_forest_err(X_test, y_test, T)

# aver_forest_e_in /= iter
# aver_forest_e_out /= iter

# print('average forest e_in:', aver_forest_e_in)
# print('average forest e_out:', aver_forest_e_out)

T = 300
rf = RandomForest(prune=True)
rf.build(X_train, y_train, T, train_cnt)

# 19
forest_e_ins = np.zeros(T)
for i in range(T):
    forest_e_ins[i] = rf.compute_forest_err(X_train, y_train, i)
plot_curve(range(T), forest_e_ins, title="19题", xlabel="树的个数", ylabel="样本错误")

# 20
forest_e_outs = np.zeros(T)
for i in range(T):
    forest_e_outs[i] = rf.compute_forest_err(X_test, y_test, i)
plot_curve(range(T), forest_e_outs, title="20题", xlabel="树的个数", ylabel="总体错误")

input("Program paused. Press ENTER to continue")
