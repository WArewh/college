import os

from kernel_ridge_regression import KernelRidgeRegression, rbf
from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file

setup()

url = "https://www.csie.ntu.edu.tw/~htlin/course/ml15fall/hw6/hw2_lssvm_all.dat"

save = os.path.join(os.path.dirname(__file__), "all19.dat")

download_file(url, save)

X, y, (cnt, dim) = load_dat(save)

T = 400

X_train, X_test = X[:T, :-1], X[T:, :-1]
y_train, y_test = y[:T], y[T:]

train_cnt, test_cnt = T, cnt - T

lmds = [0.001, 1, 1000]
gammas = [32, 2, 0.125]
paras = [(lmd,gamma) for lmd in lmds for gamma in gammas]

e_ins, e_outs = [], []

# 19、20
for para in paras:
    lmd, gamma = para
    clf = KernelRidgeRegression(lmd, gamma)

    K1 = rbf(X_train, X_train, gamma)
    K2 = rbf(X_train, X_test, gamma)

    clf.fit(K1, y_train)

    e_ins.append(clf.compute_err(K1, y_train))
    e_outs.append(clf.compute_err(K2, y_test))


print("min e_in:", min(e_ins))

print("min e_out:", min(e_outs))