import os

import numpy as np

from pla import PLA
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_histogram


setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw1/hw1_18_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw1/hw1_18_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train18.dat")
test_save = os.path.join(os.path.dirname(__file__), "test18.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

X_train = np.c_[np.ones(train_cnt), X_train]
X_test = np.c_[np.ones(test_cnt), X_test]

y_train = y_train.reshape((y_train.shape[0], 1))
y_test = y_test.reshape((y_test.shape[0], 1))

# 18
train_cnt = 2000

err = np.zeros((train_cnt))

pocket_50 = PLA(rand = True, pock = True, max_iter = 50)

for i in range(train_cnt):
    iter,best_w = pocket_50.train(X_train, y_train)
    err[i] = pocket_50.compute_err(best_w, X_test, y_test)

print("pocket_50 error:"+str(np.sum(err)/train_cnt))
plot_histogram(err, "Pocket-50", "错误率", "出现频率")

# 19
pla_50 = PLA(rand=True, max_iter = 50)

for i in range(train_cnt):
    iter,best_w = pla_50.train(X_train, y_train)
    err[i] = pla_50.compute_err(best_w, X_test, y_test)

print("pla_50 error:"+str(np.sum(err)/train_cnt))
plot_histogram(err, "PLA-50", "错误率", "出现频率")

# 20
pocket_100 = PLA(rand = True, pock = True, max_iter = 100)

for i in range(train_cnt):
    iter,best_w = pocket_100.train(X_train, y_train)
    err[i] = pocket_100.compute_err(best_w, X_test, y_test)

print("pocket_100 error:", str(np.sum(err)/train_cnt))
plot_histogram(err, "Pocket-100", "错误率", "出现频率")

input("Program paused. Press ENTER to continue")