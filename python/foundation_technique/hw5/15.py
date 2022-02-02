import os

import numpy as np
from sklearn import svm

from utils.load import load_dat
from utils.setup import setup
from utils.download import download_file
from utils.visualization import plot_curve

from helper import get_label


setup()

train_url = "http://www.amlbook.com/data/zip/features.train"
test_url = "http://www.amlbook.com/data/zip/features.test"

train_save = os.path.join(os.path.dirname(__file__), "train.dat")
test_save = os.path.join(os.path.dirname(__file__), "test.dat")

download_file(train_url, train_save)
download_file(test_url, test_save)

X_train, y_train, (train_cnt, train_dim) = load_dat(train_save, y_start=0)
X_test, y_test, (test_cnt, test_dim) = load_dat(test_save, y_start=0)


# 15
y_train_0 = get_label(y_train, 0).reshape(train_cnt)
clf = svm.SVC(kernel="linear", C=0.01, shrinking=False)
clf.fit(X_train, y_train_0)
w = clf.coef_
norm_w = np.linalg.norm(w)
print("15\n||w||:",norm_w)

# # 16、17
e_ins = np.zeros(5)
alpha_sums = np.zeros(5)
clf = svm.SVC(kernel="poly", C=0.01, degree=2, shrinking=False)
for i in range(5):
    y_train_x = get_label(y_train, 2 * i).reshape(train_cnt)
    clf.fit(X_train, y_train_x)
    pred_in = clf.predict(X_train)
    e_ins[i] = np.mean(pred_in != y_train_x)/train_cnt
    sup_idx = clf.support_
    alpha_sums[i] = np.sum(clf.dual_coef_[0] / y_train_x[sup_idx])

min_idx = np.argmin(e_ins)

print("16\nmin e_in number:", min_idx * 2,"e_in:", e_ins[min_idx])

print("17\nmax alpha sum:", np.max(alpha_sums)) # 20

# 18
norm_ws = np.zeros(5)
alpha_sums = np.zeros(5)
e_outs = np.zeros(5)
sv_cnts = np.zeros(5)

y_train_0 = get_label(y_train, 0).reshape(train_cnt)
y_test_0 = get_label(y_test, 0).reshape(test_cnt)

C = [-3, -2, -1, 0, 1]

for i in range(len(C)):
    c = 10**C[i]
    clf = svm.SVC(C=c, gamma=100, shrinking=False)
    clf.fit(X_train,y_train_0)
    w = clf.dual_coef_[0]
    norm_ws[i] = np.linalg.norm(w)
    sup_idx = clf.support_
    alpha_sums[i] = np.sum(clf.dual_coef_[0] / y_train_0[sup_idx])
    pred_out = clf.predict(X_test)
    e_outs[i] = np.mean(pred_out != y_test_0)/test_cnt
    sv_cnts[i] = sup_idx.shape[0]

plot_curve(C, norm_ws, title="18题", xlabel="C", ylabel="norm w")
plot_curve(C, alpha_sums, title="18题", xlabel="C", ylabel="alpha sum") # √
plot_curve(C, e_outs, title="18题", xlabel="C", ylabel="e_out")
plot_curve(C, sv_cnts, title="18题", xlabel="C", ylabel="sv_cnt")

# 19
y_train_0 = get_label(y_train, 0).reshape(train_cnt)
y_test_0 = get_label(y_test, 0).reshape(test_cnt)

gammas = [1, 10, 100, 1000, 10000]
e_outs = np.zeros(5)

for i in range(len(gammas)):
    clf = svm.SVC(C=0.1, gamma=gammas[i], shrinking=False)
    clf.fit(X_train,y_train_0)
    pred_out = clf.predict(X_test)
    e_outs[i] = np.mean(pred_out != y_test_0)/test_cnt

min_idx = np.argmin(e_outs)
print("19\nmin e_out gamma", gammas[min_idx])

# 20
y_train_0 = get_label(y_train, 0).reshape(train_cnt)

e_vals = np.zeros(5)
gammas = [1, 10, 100, 1000, 10000]
val_cnt = 1000

for i in range(1):
    tmp = np.c_[X_train,y_train_0]
    np.random.shuffle(tmp)
    X = tmp[:,:-1]
    y = tmp[:,-1].reshape(X.shape[0])
    X_val = X[:val_cnt]
    y_val = y[:val_cnt]
    X_train = X[val_cnt:]
    y_train = y[val_cnt:]
    for j in range(len(gammas)):
        clf = svm.SVC(C=0.1, gamma=gammas[j], shrinking=False)
        clf.fit(X_train,y_train)
        pred_val = clf.predict(X_val)
        e_vals[j] = np.mean(pred_val != y_val)/val_cnt

min_idx = np.argmin(e_vals)
print("20\nmin e_out gamma", gammas[min_idx])

input("Program paused. Press ENTER to continue")