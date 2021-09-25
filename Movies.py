import datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as scp
import seaborn as sbrn
import random as random

from matplotlib.backends.backend_pdf import PdfPages
from pandas.tools.plotting import table

path = "C:\\Users\\rayan\\Documents\\Data Science\\Movies.xlsx"
moviestable = pd.read_excel(path)

headers = ["Rank", "Title", "Studio", "Total", "Domestic", "Overseas", "Year"]
moviestable.columns = headers

Avatar = moviestable.iloc[[0]]
Starwarstfa = moviestable.iloc[[2]]

moviestable["Percent Domestic"] = moviestable["Domestic"]/moviestable["Total"]
moviestable["Percent Overseas"] = moviestable["Overseas"]/moviestable["Total"]

moviestable.head(5)
moviestable.dtypes

moviesfox = moviestable.loc[moviestable["Studio"] == "Fox"]
moviesbv = moviestable.loc[moviestable["Studio"] == "BV"]
moviesmoredomestic = moviestable.loc[moviestable["Percent Domestic"] > 0.5]

moviestable.sort_values("Domestic", ascending=False)

moviestable["Year"] = moviestable["Year"].astype("str")
yearfreq = moviestable["Year"].value_counts()
yearfreqplot = yearfreq.plot(kind = "bar", title = "Number of Movies per Year", grid = True, label = "Year")
plt.show()

yearboxplot = sbrn.boxplot(x = "Year", y ="Total", data = moviestable, width=0.3)
yearboxplot.set_xticklabels(yearboxplot.get_xticklabels(),rotation=90)
plt.show()

studioboxplot = sbrn.boxplot(x = "Studio", y = "Total", data = moviestable, width=0.5)
plt.show()

studiofreq = moviestable["Studio"].value_counts()
studiopiechart = studiofreq.plot(kind = "pie", title = "Number of Movies per Studio", grid = True, label = "Studio")
plt.show()

#Bar chart to show how much money was made per year

yearfreq = moviestable["Year"].value_counts()
numberofyears = len(yearfreq.index)
y = [None]*numberofyears

for i in range (0, numberofyears):
    subset = moviestable.loc[moviestable["Year"] == yearfreq.index[i]]
    y[i] = subset["Total"].sum()
    
yeartotalplot = plt.bar(yearfreq.index, y)
plt.xlabel("Year")
plt.xticks(rotation = 90)
plt.ylabel("Total Gross in $ millions")
plt.show()

with PdfPages("C:\\Users\\rayan\\Documents\\Data Science\\movies_pdf.pdf") as pdf:
    
    yearfreqplot = yearfreq.plot(kind = "bar", title = "Number of Movies per Year", grid = True, label = "Year")
    yearfreqplot.get_figure()
    pdf.savefig()
    plt.close()
    
    yearboxplot = sbrn.boxplot(x = "Year", y ="Total", data = moviestable, width=0.3)
    yearboxplot.set_xticklabels(yearboxplot.get_xticklabels(),rotation=90)
    yearboxplot.get_figure()
    pdf.savefig()
    plt.close()
    
    studioboxplot = sbrn.boxplot(x = "Studio", y = "Total", data = moviestable, width=0.5)
    studioboxplot.get_figure()
    pdf.savefig()
    plt.close()  
    
    studiopiechart = studiofreq.plot(kind = "pie", title = "Number of Movies per Studio", grid = True, label = "Studio")
    studiopiechart.get_figure()
    pdf.savefig()
    plt.close()
    
    totalboxplot = sbrn.boxplot(y = "Total", data = moviestable)
    totalboxplot.get_figure()
    pdf.savefig()
    plt.close()
    
    totalclassicboxplot = plt.boxplot(moviestable["Total"])
    pdf.savefig()
    plt.close()  
    
    totalhist = plt.hist(moviestable["Total"], 8, facecolor='blue', alpha = 0.8)
    plt.xlabel("Total Gross")
    plt.ylabel("Frequency")
    plt.title("Total Gross of Top 100 Movies")
    pdf.savefig()
    plt.close()
    
    lineplot = plt.plot(moviestable["Rank"], moviestable["Domestic"])
    plt.plot(moviestable["Rank"], moviestable["Overseas"])
    plt.plot(moviestable["Rank"], moviestable["Total"])
    plt.legend(["Domestic","Overseas","Total"], loc = "upper right")
    pdf.savefig()
    plt.close()
    
    yeartotalplot = plt.bar(yearfreq.index, y)
    plt.xlabel("Year")
    plt.xticks(rotation = 90)
    plt.ylabel("Total Gross in $ millions")
    pdf.savefig()
    plt.close()
