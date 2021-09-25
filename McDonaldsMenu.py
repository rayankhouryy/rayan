import pandas as pd
import numpy as np
import scipy as sp
import seaborn as sns
import matplotlib.pyplot as plt

from google.colab import files
import io

upload_file = files.upload()

data = pd.read_csv("menu.csv")

#Determine the shape of the dataset
data.shape

#View the first 5 rows
data.head(5)
#View the last 5 rows
data.tail(5)
#View a specific list of rows
data.iloc[[123, 125, 200]]
data.info()

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

#Checking that data type was changed
data.info()
#Checking that values have changed
data.iloc[[1, 4, 123, 125, 200, 258, 259]]

#Creating a column for our data set
percent_daily_calories = (data["Calories"]*100)/2000

#Inserting this column at the appropriate position
data.insert(4, "% Recommended Daily Calories", percent_daily_calories)

calories_category = []
for i in range(260):
  calories = int(data["% Recommended Daily Calories"].iloc[[i]])
  if calories <= 25:
    calories_category.append("Low")
  elif calories <= 50:
    calories_category.append("Medium")
  else:
    calories_category.append("High")

#Inserting this column at the appropriate position
data.insert(5, "Calories Category", calories_category)

data.head(5)

#Determining the number of instances of each category
data["Category"].value_counts()

#Sorting based on Calorie values 
data.sort_values("Calories", ascending = False)

#Sorting based on % of recommended dail Calories values 
data.sort_values("% Recommended Daily Calories", ascending = False)

#Creating a subset of all Breakfast items
breakfast_items = data.loc[data["Category"] == "Breakfast"]
#Determining how many breakfast items are available
breakfast_items.shape

#Creating a subset of items that have 0 Calories
zero_calories = data.loc[data["Calories"]<= 0]
#Determining how many categories contain 0 calories
zero_calories["Category"].value_counts()

#Plotting a countplot
plt.subplots(figsize=(12, 5))
sns.countplot(x = "Category", data = data)
plt.title("Bar Graph of the Different Food Categories in the McDonalds Menu")
plt.xticks(rotation=30)
plt.show()
plt.close()

#Plotting a countplot with subcategories
plt.subplots(figsize=(12, 6))
sns.countplot(x = "Category", hue = "Calories Category", data = data)
plt.title("Bar Graph of the Different Food Categories in the McDonalds Menu")
plt.xticks(rotation=30)
plt.show()
plt.close()

#PLotting a bargraph
plt.subplots(figsize=(12, 5))
sns.barplot(x = "Category", y = "Total Fat", data = data)
plt.title("Bar graph of the food categories vs. total fat")
plt.xticks(rotation=30)
plt.show()
plt.close()

plt.subplots(figsize=(12, 5))
sns.barplot(x = "Category", y = "Calories", data = data)
plt.title("Bar graph of food categories vs. calories")
plt.xticks(rotation=30)
plt.show()
plt.close()

#Plotting a histogram
plt.subplots(figsize=(12, 5))
sns.histplot(x = "Calories", data = data)
plt.title("Histogram of Calories of Food Items")
plt.show()
plt.close()

#Plotting a histogram with subcategories
plt.subplots(figsize=(12, 5))
sns.histplot(x = "Calories", hue = "Category", multiple = "stack", data = data)
plt.title("Histogram of Calories of Food Items")
plt.show()
plt.close()

#Plotting a histogram
for category in data["Category"].value_counts().index:
  print(category)
  sub_data = data.loc[data["Category"] == category]
  plt.subplots(figsize=(12, 5))
  sns.histplot(x = "Calories", data = sub_data)
  plt.title("Histogram of Calories - "+category)
  plt.show()
  plt.close()

  
 #Plotting a boxplot 
plt.subplots(figsize=(4, 5))
sns.boxplot(y = "Total Fat (% Daily Value)", data = data)
plt.title("Boxplot of Total Fat (% Daily Value)")
plt.show()
plt.close()

#Plotting a boxplot with subcategories
plt.subplots(figsize=(12, 7))
sns.boxplot(x = "Category", y = "Total Fat (% Daily Value)", data = data)
plt.title("Boxplot of Total Fat (% Daily Value)")
plt.xticks(rotation = 30)
plt.show()
plt.close()

#Plotting a boxplot with subcategories
plt.subplots(figsize=(12, 5))
sns.boxplot(x = "Category", y = "% Recommended Daily Calories", data = data)
plt.title("Boxplot of % Recommended Daily Calories")
plt.show()
plt.close()

#Plotting multiple line plots
plt.subplots(figsize = (12,5))
#sns.lineplot(x = "Calories", y = "Serving Size", data = data)
sns.lineplot(x = "Calories", y = "Total Fat", label = "Total Fat", data = data)
sns.lineplot(x = "Calories", y = "Sugars", label = "Sugars", data = data)
sns.lineplot(x = "Calories", y = "Protein", label = "Protein", data = data)
sns.lineplot(x = "Calories", y = "Carbohydrates", label = "Carbohydrates", data = data)
plt.title("Calories vs. Nutritional Elements")
plt.ylabel(" ")
plt.legend(loc = "best")
plt.show()
plt.close()

data_beverages = data.loc[data["Category"] == "Beverages"]
#Finding the coefficients of the line of best fit
slope, intercept, r_value, p_value, std_err = sp.stats.linregress(data_beverages['Calories'],data_beverages['Sugars'])

#Plotting a line of best fit
plt.subplots(figsize=(8,5)) 
sns.regplot(x = "Calories", y = "Sugars", data = data_beverages, label = "y={0:.1f}x+{1:.1f}".format(slope,intercept))
plt.title("Calories vs. Sugars for Beverages")
plt.legend()
plt.show()
plt.close()

#Plotting multiple lines of best fit
plt.figure(figsize=(15,6))
for category in data["Category"].value_counts().index:
  #Creating a subset of data for every category
  subdata = data.loc[data["Category"] == category]
  #Calculating the coefficients of the lines of best fit
  slope, intercept, r_value, p_value, std_err = sp.stats.linregress(subdata["Calories"], subdata["Sugars"])
  #Plotting the data points and lines of best fit
  sns.regplot(x = "Calories", y = "Sugars", data = subdata, 
                          label = category+", y={0:.1f}x+{1:.1f}".format(slope,intercept))
plt.title("Calories vs. Sugars for Food Categories")
plt.ylabel(" ")
plt.legend()
plt.show()
plt.close()

#Map the categories into numbers 
mapping = {"Coffee & Tea":0, "Breakfast":1, "Smoothies & Shakes":2, "Chicken & Fish":3, 
           "Beverages":4, "Beef & Pork":5, "Snacks & Sides":6, "Desserts":7, "Salads":8}
data['Category'] = data['Category'].map(mapping).astype(int)

data = data.drop("Item", axis=1)
X = data.drop("Category", axis=1)
X = data.drop("Calories Category", axis = 1)
X.head()
Y.head()

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
from sklearn.svm import SVC 
model = SVC()
model.fit(X_train, Y_train)
labels = model.predict(X_test)

from sklearn.metrics import accuracy_score
accuracy_score(Y_test, labels)

from sklearn.metrics import confusion_matrix

mat = confusion_matrix(Y_test, labels)
sns.heatmap(mat.T, square = True, annot=True, fmt = 'd', cbar=False)
plt.xlabel("True Label")
plt.ylabel("predicted label")
