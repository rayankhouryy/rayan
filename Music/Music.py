import datetime

import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sbn
import random as random

from matplotlib.backends.backend_pdf import PdfPages

#Importing dataset and renaming columns

path = "C:\\Users\\rayan\\Documents\\Data Science\\Music.xlsx"
musictable = pd.read_excel(path)
headers = ["Artist","Song", "Duration", "Loudness","BPM", "Endofin", "Startofout", "Familiarity", "Buzz", "Terms"]
musictable.columns = headers

#Identifying some rows

hell_foofighters = musictable.iloc[[141]]
hipsdontliew_shakira = musictable.iloc[[142]]
shameless_alltimelow = musictable.iloc[[372]]
newage_daniela = musictable.iloc[[207]]

#Adding some new columns

musictable["Meatofsong"] = musictable["Startofout"]-musictable["Endofin"]

#Print first few rows of dataset
musictable.head(5)

#Identifying types of data

musictable.dtypes

#Adding some filters

musicbyshakira = musictable.loc[musictable["Artist"] == "Shakira"]
loudmusic = musictable.loc[musictable["Loudness"] > musictable["Loudness"].mean()]
longmusic = musictable.loc[musictable["Duration"] > 240]

#Some ordered versions of the data set

musicbyartist = musictable.sort_values("Artist")
musicbyterms = musictable.sort_values("Terms")
musicbyduration = musictable.sort_values("Duration", ascending=False)
musicbybpm = musictable.sort_values("BPM", ascending=False)

#Printing some interesting values

print("Longest song is: \n", musicbyduration.iloc[[0]])
print("\n \n")
print("Shortest song is: \n", musicbyduration.iloc[[-1]])

#Top 10 most common genres

termscount = musictable["Terms"].value_counts()
top10terms = termscount.head(10)
top10terms

#Boxplot of BPM for common genres

top10termstable = musictable.loc[musictable["Terms"].isin(top10terms.index)]
bpmboxplot = sbn.boxplot(x=top10termstable["Terms"], y=top10termstable["BPM"])
bpmboxplot.set_xticklabels(bpmboxplot.get_xticklabels(), rotation=90)

#Boxplot of Duration for common genres

durationboxplot = sbn.boxplot(x=top10termstable["Terms"], y=top10termstable["Duration"])
durationboxplot.set_xticklabels(durationboxplot.get_xticklabels(), rotation=90)

#Boxplot of Loudness for common genres

loudnessboxplot = sbn.boxplot(x=top10termstable["Terms"], y=top10termstable["Loudness"])
loudnessboxplot.set_xticklabels(loudnessboxplot.get_xticklabels(), rotation=90)

#Boxplot of Familiarity for common genres

familiarityboxplot = sbn.boxplot(x=top10termstable["Terms"], y=top10termstable["Familiarity"])
familiarityboxplot.set_xticklabels(familiarityboxplot.get_xticklabels(), rotation=90)

#Histogram of durations, loudness, bpm, familiarity

music2 = musicbyduration.iloc[10:(len(musicbyduration)-1)]

durationhist = plt.hist(music2["Duration"], 20, facecolor='blue', alpha = 0.8)
plt.xlabel("Duration")
plt.ylabel("Frequency")
plt.title("Distribution of Song Durations")
plt.show()

loudnesshist = plt.hist(musictable["Loudness"], 8, facecolor='blue', alpha = 0.8)
plt.xlabel("Loudness")
plt.ylabel("Frequency")
plt.title("Distribution of Song Loudness")
plt.show()

BPMhist = plt.hist(musictable["BPM"], 8, facecolor='blue', alpha = 0.8)
plt.xlabel("BPM")
plt.ylabel("Frequency")
plt.title("Distribution of Song BPMs")
plt.show()

#Some scatter plots with their regression lines

x = musicbyduration["Duration"].iloc[10:(len(musicbyduration)-1)]
y = musicbyduration["BPM"].iloc[10:(len(musicbyduration)-1)]
b, m = np.polyfit(x, y, 1)
plt.scatter(x, y)
plt.plot(x, b + m * x, color="red")
plt.xlim(-100, 1400)
plt.ylim(-10, 270)
plt.show()

x1 = musictable["Loudness"]
y1 = musictable["Familiarity"]
b1, m1 = np.polyfit(x1, y1, 1)
plt.scatter(x1, y1)
plt.plot(x1, b1 + m1 * x1, color="red")
plt.show()

x2 = musicbyduration["Duration"].iloc[10:(len(musicbyduration)-1)]
y2 = musicbyduration["Endofin"].iloc[10:(len(musicbyduration)-1)]
b2, m2 = np.polyfit(x2, y2, 1)
plt.scatter(x2, y2)
plt.plot(x2, b2 + m2 * x2, color="red")
plt.xlim(-100, 1400)
plt.ylim(-10, 50)
plt.show()


with PdfPages("C:\\Users\\rayan\\Documents\\Data Science\\music_pdf.pdf") as pdf:
    
    bpmboxplot = sbn.boxplot(x=top10termstable["Terms"], y=top10termstable["BPM"])
    bpmboxplot.set_xticklabels(bpmboxplot.get_xticklabels(), rotation=90)
    plt.title("BPM per Genre")
    bpmboxplot.get_figure()
    pdf.savefig()
    plt.close()
    
    durationboxplot = sbn.boxplot(x=top10termstable["Terms"], y=top10termstable["Duration"])
    durationboxplot.set_xticklabels(durationboxplot.get_xticklabels(), rotation=90)
    plt.title("Duration per Genre")
    durationboxplot.get_figure()
    pdf.savefig()
    plt.close()
    
    loudnessboxplot = sbn.boxplot(x=top10termstable["Terms"], y=top10termstable["Loudness"])
    loudnessboxplot.set_xticklabels(loudnessboxplot.get_xticklabels(), rotation=90)
    plt.title("Loudness per Genre")
    loudnessboxplot.get_figure()
    pdf.savefig()
    plt.close()
    
    familiarityboxplot = sbn.boxplot(x=top10termstable["Terms"], y=top10termstable["Familiarity"])
    familiarityboxplot.set_xticklabels(familiarityboxplot.get_xticklabels(), rotation=90)
    plt.title("Familiarity per Genre")
    familiarityboxplot.get_figure()
    pdf.savefig()
    plt.close()
    
    plt.pie(top10terms, labels=top10terms.index, autopct='%1.0f%%', pctdistance=1.2, labeldistance=1.3)
    plt.title("Distribution of Genres")
    pdf.savefig()
    plt.close()
    
    plt.bar(top10artist.index, top10artist, align="center")
    plt.xticks(rotation = 90)
    plt.ylabel("Number of Songs per Artist")
    pdf.savefig()
    plt.close()
    
    durationhist = plt.hist(music2["Duration"], 20, facecolor='blue', alpha = 0.8)
    plt.xlabel("Duration")
    plt.ylabel("Frequency")
    plt.title("Distribution of Song Durations")
    pdf.savefig()
    plt.close()
    
    loudnesshist = plt.hist(musictable["Loudness"], 8, facecolor='blue', alpha = 0.8)
    plt.xlabel("Loudness")
    plt.ylabel("Frequency")
    plt.title("Distribution of Song Loudness")
    pdf.savefig()
    plt.close()
    
    BPMhist = plt.hist(musictable["BPM"], 8, facecolor='blue', alpha = 0.8)
    plt.xlabel("BPM")
    plt.ylabel("Frequency")
    plt.title("Distribution of Song BPMs")
    pdf.savefig()
    plt.close()
    
    x = musicbyduration["Duration"].iloc[10:(len(musicbyduration)-1)]
    y = musicbyduration["BPM"].iloc[10:(len(musicbyduration)-1)]
    b, m = np.polyfit(x, y, 1)
    plt.scatter(x, y)
    plt.plot(x, b + m * x, color="red")
    plt.xlim(-100, 1400)
    plt.ylim(-10, 270)
    plt.xlabel("Duration (sec)")
    plt.ylabel("BPM")
    plt.title("Duration vs. BPM")
    pdf.savefig()
    plt.close()
    
    x1 = musictable["Loudness"]
    y1 = musictable["Familiarity"]
    b1, m1 = np.polyfit(x1, y1, 1)
    plt.scatter(x1, y1)
    plt.plot(x1, b1 + m1 * x1, color="red")
    plt.xlabel("Loudness")
    plt.ylabel("Familiarity")
    plt.title("Loudness vs. Familiarity")
    pdf.savefig()
    plt.close()
    
    x2 = musicbyduration["Duration"].iloc[10:(len(musicbyduration)-1)]
    y2 = musicbyduration["Endofin"].iloc[10:(len(musicbyduration)-1)]
    b2, m2 = np.polyfit(x2, y2, 1)
    plt.scatter(x2, y2)
    plt.plot(x2, b2 + m2 * x2, color="red")
    plt.xlim(-100, 1400)
    plt.ylim(-10, 50)
    plt.xlabel("Duration (sec)")
    plt.ylabel("End of Fade In")
    plt.title("Duration vs. End of Fade In") 
    pdf.savefig()
    plt.close()
