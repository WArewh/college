import os

import numpy as np

from k_means import KMeans
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_curve

setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw8/hw8_nolabel_train.dat"

train_save = os.path.join(os.path.dirname(__file__), "train19.dat")

download_file(train_url, train_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save,y=False)

T = 500
K = [2, 4, 6, 8, 10]

aver_e_ins = np.zeros_like(K, dtype=np.float)

for i in range(len(K)):
    total_e_in = 0
    clf = KMeans(K[i])
    for j in range(T):
        centers, y = clf.fit(X_train)
        total_e_in += clf.compute_err(centers, X_train, y)

    aver_e_ins[i] = total_e_in / T

# 20
plot_curve(K, aver_e_ins, title="20题", xlabel="K", ylabel="错误率")
print(aver_e_ins)

input("Program paused. Press ENTER to continue")