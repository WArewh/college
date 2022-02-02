import os

import numpy as np

from random_forest import RandomForest
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_curve, plot_histogram


setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw7/hw7_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw7/hw7_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train.dat")
test_save = os.path.join(os.path.dirname(__file__), "test.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

# coursera 16-18题 300->30 100->10 结果差不多
# T = 30
# iter = 10
# aver_trees_e_in = 0.0
# aver_forest_e_in = 0.0
# aver_forest_e_out = 0.0

# for i in range(iter):
#     rf = RandomForest()
#     rf.build(X_train, y_train, T, train_cnt)
#     aver_trees_e_in += rf.compute_tree_err(X_train, y_train)
#     aver_forest_e_in += rf.compute_forest_err(X_train, y_train, T)
#     aver_forest_e_out += rf.compute_forest_err(X_test, y_test, T)

# aver_trees_e_in /= iter
# aver_tree_e_in = np.mean(aver_trees_e_in)
# aver_forest_e_in /= iter
# aver_forest_e_out /= iter

# print('average tree e_in:', aver_tree_e_in)
# print('average forest e_in:', aver_forest_e_in)
# print('average forest e_out:', aver_forest_e_out)

# # 30000 -> 100
T = 100
rf = RandomForest()
rf.build(X_train, y_train, T, train_cnt)

# 16
tree_e_ins = rf.compute_tree_err(X_train, y_train)
plot_histogram(tree_e_ins, title="16题", xlabel="错误", ylabel="出现次数")

# 17
forest_e_ins = np.zeros(T)
for i in range(T):
    forest_e_ins[i] = rf.compute_forest_err(X_train, y_train, i)
plot_curve(range(T), forest_e_ins, title="17题", xlabel="树的个数", ylabel="样本错误")

# 18
forest_e_outs = np.zeros(T)
for i in range(T):
    forest_e_outs[i] = rf.compute_forest_err(X_test, y_test, i)
plot_curve(range(T), forest_e_outs, title="18题", xlabel="树的个数", ylabel="总体错误")

input("Program paused. Press ENTER to continue")