import numpy as np
import scipy as sp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from google.colab import files
import io
upload_file = files.upload()

data = pd.read_csv("menu.csv")
data.head(1)

#Cleaning the Serving Size column
for i in range(260):
  item_list = []
  item_list2 = []
  item = str(data["Serving Size"].iloc[[i]])
  if "(" in item:
    item_list = item.split("(")
    item_list2 = item_list[1].split(" ")
    data["Serving Size"].iloc[[i]] = float(item_list2[0])
  else:
    item_list = item.split(" ")
    data["Serving Size"].iloc[[i]] = float(item_list[0])*29.57

#Changing the serving size column to float
data["Serving Size"] = data["Serving Size"].astype("float")

data.drop("Item", axis = 1, inplace=True)
data["Category"].value_counts().index

mapping = {"Coffee & Tea":0, "Breakfast":1, "Smoothies & Shakes":2, "Chicken & Fish":3, 
           "Beverages":4, "Beef & Pork":5, "Snacks & Sides":6, "Desserts":7, "Salads":8}
data['Category'] = data['Category'].map(mapping).astype(int)

X = data.drop("Calories", axis=1)
y = data["Calories"]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
from sklearn.linear_model import LinearRegression # 1. choose model class
model = LinearRegression()                        # 2. instantiate model
model.fit(X_train, y_train)                         # 3. fit model to data
y_model = model.predict(X_test)                    # 4. predict on new data

from sklearn import metrics
import math

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_model))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_model))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_model)))

#We are on average 5.6 away from the true number of Calories when making predictions on our test data set
model.score(X_train, y_train)
model.score(X_test, y_test)
from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators=200, random_state=0)  
regressor.fit(X_train, y_train)  
y_model = regressor.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_model))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_model))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_model)))

regressor.score(X_train, y_train)
regressor.score(X_test, y_test)
