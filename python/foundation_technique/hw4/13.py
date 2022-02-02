import os

import numpy as np

from linear_regression import LinearRegression
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_curve


setup()

train_url = "http://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw4/hw4_train.dat"
test_url = "http://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw4/hw4_test.dat"

train_save = os.path.join(os.path.dirname(__file__),"train.dat")
test_save = os.path.join(os.path.dirname(__file__),"test.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

X_train = np.c_[np.ones(train_cnt), X_train]
X_test = np.c_[np.ones(test_cnt), X_test]

y_train = y_train.reshape((y_train.shape[0],1))
y_test = y_test.reshape((y_test.shape[0],1))

# 13
lmd = 10
lr_10 = LinearRegression(lmd)
w, e_in = lr_10.train(X_train, y_train)
e_out = lr_10.test(w, X_test, y_test)
print("question 13")
print("lambda = 10 e_in: ", e_in)
print("lambda = 10 e_out: ", e_out)

# 14、15
log10_lmds = list(range(3, -10, -1))
lmds = [10**i for i in log10_lmds]

e_ins = np.zeros(len(lmds))
e_outs = np.zeros(len(lmds))

for i in range(len(lmds)):
    lr_x = LinearRegression(lmds[i])
    w, e_ins[i] = lr_x.train(X_train, y_train)
    e_outs[i] = lr_x.test(w, X_test, y_test)


plot_curve(log10_lmds, e_ins, 0, label="e_ins")
plot_curve(log10_lmds, e_outs, 0, label="e_outs")
min_e_in_i = np.argmin(e_ins)
min_e_out_i = np.argmin(e_outs)

print("question 14")
print(
    "lmd =", lmds[min_e_in_i],
    "minimum e_in =", e_ins[min_e_in_i],
    "e_out =", e_outs[min_e_in_i])

print("question 15")
print(
    "lmd =", lmds[min_e_out_i],
    "minimum e_in =", e_ins[min_e_out_i],
    "minimum e_out = ", e_outs[min_e_out_i])

input("Program paused. Press ENTER to continue")