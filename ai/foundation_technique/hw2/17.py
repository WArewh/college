import numpy as np

from generate import generate_data
from decision_stump import decision_stump
from utils.setup import setup
from utils.visualization import plot_histogram


setup()
# 17
data_range = (-1, 1)
size = 20
noise = 0.2

iter = 5000
e_ins = np.zeros(iter)
e_outs = np.zeros(iter)

for i in range(iter):
    (X, y) = generate_data(data_range, size, noise)
    (theta,s,e_in) = decision_stump(X,y)
    e_ins[i] = e_in
    e_outs[i] = 0.5 + 0.3 * s * (np.abs(theta) - 1)

aver_e_in = np.sum(e_ins)/iter
print("average e_in: ",aver_e_in)
plot_histogram(e_ins, "样本误差直方图", "样本误差", "出现次数")

# 18
aver_e_out = np.sum(e_outs)/iter
print("average e_out: ",aver_e_out)
plot_histogram(e_ins, "外部误差直方图", "外部误差", "出现次数")


input("Program paused. Press ENTER to continue")