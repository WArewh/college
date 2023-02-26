import os

import numpy as np

from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file

setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw8/hw8_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw8/hw8_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train11.dat")
test_save = os.path.join(os.path.dirname(__file__), "test11.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

gamma = [0.001, 0.1, 1, 10, 100]