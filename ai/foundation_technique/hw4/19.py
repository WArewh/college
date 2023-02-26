import os

import numpy as np

from linear_regression import LinearRegression
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file


setup()

train_url = "http://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw4/hw4_train.dat"
test_url = "http://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw4/hw4_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train.dat")
test_save = os.path.join(os.path.dirname(__file__), "test.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

X_train = np.c_[np.ones(train_cnt), X_train]
X_test = np.c_[np.ones(test_cnt), X_test]

y_train = y_train.reshape((y_train.shape[0], 1))
y_test = y_test.reshape((y_test.shape[0], 1))

log10_lmds = list(range(3, -10, -1))
lmds = [10**i for i in log10_lmds]

# 19
e_cvs = np.zeros(len(lmds))
for i in range(len(lmds)):
    lr_x = LinearRegression(lmds[i])
    e_cvs[i] = lr_x.cross_val(X_train, y_train, 5)

min_e_cv_i = np.argmin(e_cvs)

print("question 19")
print(
    "lmd =", lmds[min_e_cv_i],
    "minimum e_cv =", e_cvs[min_e_cv_i])

# 20
best_lmd = lmds[min_e_cv_i]
lr_best = LinearRegression(best_lmd)
best_w, e_in = lr_best.train(X_train, y_train)
e_out = lr_best.test(best_w, X_test, y_test)

print("question 20")
print(
    "lmd =",best_lmd,
    "e_in =", e_in,
    "e_out =", e_out)

input("Program paused. Press ENTER to continue")