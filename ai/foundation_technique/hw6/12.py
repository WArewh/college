import os

import numpy as np

from adaboost_stump import adaboost,predict, compute_err
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_curve, plot_scatter


setup()

train_url = "https://www.csie.ntu.edu.tw/~htlin/mooc/datasets/mltech/hw2_adaboost_train.dat"
test_url = "https://www.csie.ntu.edu.tw/~htlin/mooc/datasets/mltech/hw2_adaboost_test.dat"

train_save = os.path.join(os.path.dirname(__file__), "train12.dat")
test_save = os.path.join(os.path.dirname(__file__), "test12.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save)

T = 300
thetas, alphas, signs, e_ins, idxs, u_sums, eps = adaboost(X_train, y_train, T)

# 12
print("12\nmin E_in:",e_ins[0])
print("alpha(1):",alphas[0])

# 13
plot_curve(range(T), e_ins, title="13题", xlabel="t", ylabel="g E_in")

# 14
G_e_ins = np.zeros(T)
for i in range(T):
    pred_in = predict(thetas[:i], signs[:i], idxs[:i], alphas[:i], X_train)
    G_e_ins[i] = compute_err(pred_in, y_train)

plot_curve(range(T), G_e_ins, title="14题", xlabel="t", ylabel="G E_in")
print("14\nG E_in:", G_e_ins[-1])

# 15
print("15\nU2:", u_sums[1])
print("UT:", u_sums[-1])
plot_curve(range(T), u_sums, title="15题", xlabel="t", ylabel="$u^{t}_n$")

# 16
plot_curve(range(T), eps, title="16题", xlabel="t", ylabel="epsilon_t")
print("16\nmin epsilon:", np.min(eps))

# 17、18
G_e_outs = np.zeros(T)
for i in range(T):
    pred_out = predict(thetas[:i], signs[:i], idxs[:i], alphas[:i], X_test)
    G_e_outs[i] = compute_err(pred_out, y_test)

print("17\nG1 E_out", np.min(G_e_outs[1]))
plot_curve(range(T), e_ins, title="18题", xlabel="t", ylabel="G E_out")
# 和网上的答案差了一点，画了决策曲线也没发现有太大问题
print("18\nGT E_out", G_e_outs[-1])

# 决策曲线
# import matplotlib.pyplot as plt

# pos = np.where(y_train == 1)
# neg = np.where(y_train == -1)
# plot_scatter(X_train[pos, 0], X_train[pos, 1], num=300, label="+1")
# plot_scatter(X_train[neg, 0], X_train[neg, 1], num=300, label="-1")

# x_min, x_max = X_train[:, 0].min() - 0.1, X_train[:, 0].max() + 0.1
# y_min, y_max = X_train[:, 1].min() - 0.1, X_train[:, 1].max() + 0.1
# h = 0.01
# x1, x2 = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
# z = predict(thetas[:i], signs[:i], idxs[:i], alphas[:i], np.c_[x1.ravel(), x2.ravel()])
# z = z.reshape(x1.shape)
# plt.figure(300)
# plt.contour(x1, x2, z, levels=[0], colors=['blue'])


input("Program paused. Press ENTER to continue")