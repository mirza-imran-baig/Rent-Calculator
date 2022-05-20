import time
import pandas as pd
import numpy as np
from clean_data import CleanData
from encoding import EncodeData
from correlation import Correlation
from split import SplitData
from sklearn import linear_model
from sklearn import metrics
from sklearn import model_selection
from sklearn import feature_selection
import scipy

class LinearReg():
    def __init__(self, X_train, X_test):
        self.__X_train = X_train
        self.__X_test = X_test
        self.__linearRegression = linear_model.LinearRegression(n_jobs=-1)

    def fit_(self):
        X = self.__X_train.drop('rent_amount_boxcox',axis=1)
        y = self.__X_train['rent_amount_boxcox']
        folds = model_selection.KFold(n_splits = 5, shuffle = True, random_state = 100)
        scores = model_selection.cross_val_score(self.__linearRegression, X, y, scoring='r2', cv=folds)
        return scores.mean()    

    def predict(self):
        X = self.__X_test.drop('rent_amount_boxcox',axis=1)
        y = self.__X_test['rent_amount_boxcox']
        ypred = self.__linearRegression.predict(X)
        print('MAE:', metrics.mean_absolute_error(y, ypred))
        print('MSE:', metrics.mean_squared_error(y, ypred))
        print('RMSE:', np.sqrt(metrics.mean_squared_error(y, ypred)))
        print('r2_score:', metrics.r2_score(y, ypred))  
        

    def test(self, lambda_):
        test_data = [[2, 3, 2, 2, 0, 0, 0, 2, 2, 91]]
        ypred = self.__linearRegression.predict(test_data)
        res = scipy.special.inv_boxcox(ypred, lambda_)
        res_predict = scipy.special.inv_boxcox(self.__X_test['rent_amount_boxcox'].head(1).values,lambda_)
        return res, self.__X_test.drop('rent_amount_boxcox',axis=1).head(1), res_predict
        


start = time.time()
clean_data = CleanData("house_price.csv")
data = clean_data.fit()
encode_data = EncodeData(data)  
data = encode_data.fit()
corr = Correlation(data)
data = corr.corr_fit()
split = SplitData(data)
X, x = split.fit()
para_x = split.getParameters()
linear = LinearReg(X, x)
print(linear.fit_())
#linear.predict()
#print(linear.test(para_x))

print("Total time taken:", time.time() - start)