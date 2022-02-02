import os
import numpy as np

from decision_stump import decision_stump,compute_err
from utils.setup import setup
from utils.download import download_file
from utils.load import load_dat


setup()

# 19
train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml14fall/hw2/hw2_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml14fall/hw2/hw2_test.dat"

train_save = os.path.join(os.path.dirname(__file__),"train19.dat")
test_save = os.path.join(os.path.dirname(__file__),"test19.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train,y_train,(train_cnt, train_dim) = load_dat(train_save)
X_test,y_test,(test_cnt, test_dim) = load_dat(test_save)

thetas = np.zeros(train_dim)
signs = np.zeros(train_dim)
e_ins = np.zeros(train_dim)

for i in range(train_dim):
    X = X_train[:, i]
    y = y_train
    (thetas[i], signs[i], e_ins[i]) = decision_stump(X, y)
    best_dim = np.argmin(e_ins)

print("e_in:", e_ins[best_dim])

err = compute_err(thetas[best_dim], signs[best_dim], X_test[:, best_dim], y_test)

print("test err:", err)

input("Program paused. Press ENTER to continue")
