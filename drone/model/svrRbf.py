import numpy as np
from sklearn.svm import SVR
# import matplotlib.pyplot as plt
import matplotlib.pyplot


def learn(x, y, c=1e3, gamma=0.1):
    svr_rbf = SVR(kernel='rbf', C=c, gamma=gamma)
    model = svr_rbf.fit(x, y)
    return model


def predict(model, xx):
    return model.predict(xx)


def someTest():
    X = np.sort(5 * np.random.rand(40, 1), axis=0)
    y = np.sin(X).ravel()
    y[::5] += 3 * (0.5 - np.random.rand(8))
    predictedY = predict(learn(X, y), X)
    lw = 2
    plt.scatter(X, y, color='darkorange', label='data')
    plt.hold('on')
    plt.plot(X, predictedY, color='navy', lw=lw, label='RBF model')
    plt.xlabel('data')
    plt.ylabel('target')
    plt.title('Support Vector Regression')
    plt.legend()
    plt.show()


someTest()
