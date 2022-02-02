import os

import numpy as np

from pla import PLA
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_histogram


setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw1/hw1_15_train.dat"
train_save = os.path.join(os.path.dirname(__file__), "train15.dat")

download_file(train_url, train_save)
X,y,(cnt,dim) = load_dat(train_save)

X = np.c_[np.ones(X.shape[0]),X]
y = y.reshape((y.shape[0],1))

# 15
navi_pla = PLA()
iter,w = navi_pla.train(X,y)
print("15 answer:"+str(iter))

# 16
iter_count = 2000
iters = np.zeros(iter_count)

rand_pla = PLA(rand=True)

for i in range(iter_count):
    iters[i],w = rand_pla.train(X,y)

plot_histogram(iters, "pla 2000次", "迭代次数", "出现频率")
print("16 plot finish")

# 17
total_iter = 0
rand_eta_pla = PLA(eta=0.5, rand=True)

for i in range(iter_count):
    iter,w= rand_eta_pla.train(X,y)
    total_iter += iter


print("17 answer:", total_iter/iter_count)

input("Program paused. Press ENTER to continue")
