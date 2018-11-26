import numpy as np

data = ["fixed acidity","volatile acidity","citric acid","residual sugar",\
        "chlorides","free sulfur dioxide","total sulfur dioxide","density","pH",\
        "sulphates","alcohol","quality"]
header = ['1', '2', '3']
header = np.array(header, dtype=np.unicode_)
data = np.array([header, [1,2,3], [4,5,67], [7,8,9]])
data[:][2] = 9000
print(data)
