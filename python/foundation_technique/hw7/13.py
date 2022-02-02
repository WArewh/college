import os

import numpy as np

from decision_tree import DecisionTree
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file

setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw7/hw7_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw7/hw7_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train.dat")
test_save = os.path.join(os.path.dirname(__file__), "test.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

tree = DecisionTree()
tree.build(X_train, y_train)

# 13 替换为coursera 13题
cnt = tree.count_internal_nodes()
print('13\nThe number of internal nodes:',cnt)

# 14
e_in = tree.compute_err(X_train,y_train)
print('14\nG e_in:', e_in)

# 15
e_out = tree.compute_err(X_test,y_test)
print('15\nG e_out:', e_out)

input("Program paused. Press ENTER to continue")