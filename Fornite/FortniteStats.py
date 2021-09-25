import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import random as rand
import seaborn as sbn

from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages

path = "C:\\Users\\rayan\\Documents\\Data Science\\FortniteStats.xlsx"
fortnite = pd.read_excel(path)
fortnite.head(5)

for column in fortnite.columns[1:7]:
    Max = fortnite.loc[fortnite[column] == fortnite[column].max()]
    print("The player with the highest" , column, "is: ")
    print (Max)
    print("\n \n")
    
#Creating table with normalized values

fortnite2 = pd.read_excel(path)
for column in fortnite2.columns[1:7]:
    fortnite2[column] = (fortnite2[column] - fortnite2[column].mean()) / fortnite2[column].std()
fortnite2.head(5)

for column in fortnite.columns[1:6]:
    x = fortnite["Score"]
    y = fortnite[column]
    b, m = np.polyfit(x,y,1)
    fit_fn = m + b*x
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(x, y)
    plt.plot(x,y, '.', label = (column, "{0:.2f}".format(r_value), "{0:.2f}".format(p_value)))
    plt.plot(x, fit_fn, color = "red", label = "y={0:.1f}x+{1:.1f}".format(b,m))
    plt.xlabel("Score")
    plt.xticks(rotation = 90)
    plt.ylabel(column)
    plt.legend()
    title = "Score vs. "+column
    plt.title(title)
    #plt.show()
    #plt.close()
    
for column in fortnite.columns[1:7]:
    plt.figure(figsize=(15,6))
    plt.boxplot(fortnite[column], vert = False)
    plt.title(column)
    plt.show()
    plt.close()
    
plt.figure(figsize=(15,6))
for column in fortnite.columns[1:6]:
    slope, intercept, r_value, p_value, std_err = stats.linregress(fortnite["Score"],fortnite[column])
    Plot1 = sbn.regplot(fortnite["Score"], fortnite[column], data = fortnite, 
                        label = (column,"{0:.2f}".format(r_value),"{0:.2f}".format(p_value)),
                        marker = '.')
plt.title("Score")
plt.ylabel(" ")
plt.legend()
plt.show()

plt.figure(figsize=(15,6))
for column in fortnite2.columns[1:6]:
    slope, intercept, r_value, p_value, std_err = stats.linregress(fortnite2["Score"],fortnite2[column])
    Plot1 = sbn.regplot(fortnite2["Score"], fortnite2[column], data = fortnite2, 
                        label = (column,"{0:.2f}".format(r_value),"{0:.2f}".format(p_value)),
                        marker = '.')
plt.title("Score")
plt.ylabel(" ")
plt.legend()
plt.show()

with PdfPages("C:\\Users\\rayan\\Documents\\Data Science\\fortnite.pdf") as pdf:
    
    for column in fortnite.columns[1:6]:
        x = fortnite["Score"]
        y = fortnite[column]
        b, m = np.polyfit(x,y,1)
        fit_fn = m + b*x
        slope, intercept, r_value, p_value, std_err = sp.stats.linregress(x, y)
        plt.plot(x,y, '.', label = (column, "{0:.2f}".format(r_value), "{0:.2f}".format(p_value)))
        plt.plot(x,y, '.')
        plt.plot(x, fit_fn, color = "red", label = "y={0:.1f}x+{1:.1f}".format(b,m))
        plt.xlabel("Score")
        plt.xticks(rotation = 90)
        plt.ylabel(column)
        plt.legend()
        title = "Score vs. "+column
        plt.title(title)
        pdf.savefig(bbox_inches = "tight")
        plt.close()
    
    for column in fortnite.columns[1:7]:
        plt.figure(figsize=(15,6))
        plt.boxplot(fortnite[column], vert = False)
        plt.title(column)
        pdf.savefig(bbox_inches = "tight")
        plt.close()
    
    plt.figure(figsize=(15,6))
    for column in fortnite2.columns[1:6]:
        slope, intercept, r_value, p_value, std_err = stats.linregress(fortnite2["Score"],fortnite2[column])
        Plot1 = sbn.regplot(fortnite2["Score"], fortnite2[column], data = fortnite2, 
                            label = (column,"{0:.2f}".format(r_value),"{0:.2f}".format(p_value)),marker = '.')
    plt.title("Score")
    plt.ylabel(" ")
    plt.legend()
    pdf.savefig(bbox_inches = "tight")
    plt.close()
