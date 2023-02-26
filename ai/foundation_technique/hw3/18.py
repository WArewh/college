import os
import numpy as np

from logistic_regression import LogisticRegression
from utils.setup import setup
from utils.download import download_file
from utils.load import load_dat

setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw3/hw3_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw3/hw3_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train18.dat")
test_save = os.path.join(os.path.dirname(__file__), "test18.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train,y_train,(train_cnt, train_dim) = load_dat(train_save)
X_test,y_test,(test_cnt, test_dim) = load_dat(test_save)

X_train = np.c_[np.ones(train_cnt), X_train]
X_test = np.c_[np.ones(test_cnt), X_test]

y_train = y_train.reshape((train_cnt, 1))
y_test = y_test.reshape((test_cnt, 1))

# 18
max_iter = 2000
lr = LogisticRegression()
best_w = lr.train(X_train, y_train, max_iter) 
err = lr.test(best_w, X_test, y_test)
print("18 err: ",err)

# 19
lr_eta = LogisticRegression(eta=0.01)
best_w = lr_eta.train(X_train, y_train, max_iter) 
err = lr_eta.test(best_w, X_test, y_test)
print("19 err: ",err)

# 20
lr_rand = LogisticRegression(rand_grad=True)
best_w = lr_rand.train(X_train, y_train, max_iter) 
err = lr_rand.test(best_w, X_test, y_test)
print("20 err: ",err)