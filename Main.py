from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import base64
os.environ["PYTHONIOENCODING"] = "utf-8"

main = Tk()
main.call('encoding', 'system', 'utf-8')
main.title("OPINION MINING FOR FEEDBACK MANAGEMENT SYSTEM")
main.geometry("1300x1200")

sid = SentimentIntensityAnalyzer()

def getCount(sentence):
    pos = []
    neg = []
    neu = []
    arr = sentence.split(' ')
    for i in range(len(arr)):
        word = arr[i].strip()
        if (sid.polarity_scores(word)['compound']) >= 0.5:
            pos.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.5:
            neg.append(word)
        else:
            neu.append(word)
    return pos,neg,neu      

global filename
global sentence
global positive_mean
global negative_mean
global positive_reviews
global negative_reviews

def module1():
    text.delete('1.0', END)
    #print(base64.b64encode(tf1.get().encode("utf-8")))
    #name = bytes(tf1.get(),"unicode_escape")
    #print(name)
    sentence = tf1.get()

    sentiment_dict = sid.polarity_scores(sentence)
    negative = sentiment_dict['neg']
    positive = sentiment_dict['pos']
    neutral = sentiment_dict['neu']
    compound = sentiment_dict['compound']
    text.insert(END,"Input Sentence : "+sentence+"\n\n")
    text.insert(END,"Positive : "+str(positive)+"\n")
    text.insert(END,"Negative : "+str(negative)+"\n")
    text.insert(END,"Neutral : "+str(neutral)+"\n")
    text.insert(END,"Compound : "+str(compound)+"\n")
    result = ''
    if compound >= 0.05 : 
        result = 'Positive' 
  
    elif compound <= - 0.05 : 
        result = 'Negative' 
  
    else : 
        result = 'Neutral'
    pos,neg,neu = getCount(sentence)
    text.insert(END,sentence+' CLASSIFIED AS '+result+"\n\n")
    text.insert(END,'Positive Words : '+str(pos)+"\n")
    text.insert(END,'Negative Words : '+str(neg)+"\n")
    text.insert(END,'Neutral Words  : '+str(neu)+"\n")
    tf1.delete(0,'end')

    height = [len(pos),len(neg),len(neu)]
    bars = ('Positive Words', 'Negative Words','Neutral Words')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()
    
def upload():
    global filename
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "dataset")

def positiveReviews():
    global positive_reviews
    global positive_mean
    positive_reviews = 0
    text.delete('1.0', END)
    query = tf2.get()
    train = pd.read_csv(filename,encoding='utf8')
    count = 0
    total = 0
    cols = train.shape[1]
    m = 0
    n = 0
    if cols == 2:
        m = 0
        n = 1
    else:
        m = 1
        n = 16
    for i in range(len(train)):
        name = str(train.get_value(i,m,takeable = True))
        sentence = str(train.get_value(i,n,takeable = True))
        if query in name:
            total = total + 1
            sentiment_dict = sid.polarity_scores(sentence)
            compound = sentiment_dict['compound']
            positive = sentiment_dict['pos']
            if compound >= 0.05 :
                text.insert(END,str(sentence.encode('UTF-8'))+" == "+str(positive)+"\n")
                count = count + 1
    positive_reviews = count            
    positive_mean = count/total            
    text.insert(END,"\n\nTotal Reviews    : "+str(total)+"\n")
    text.insert(END,"Positive Reviews : "+str(count)+"\n\n\n")
    text.see(END)
    
def negativeReviews():
    global negative_reviews
    global negative_mean
    negative_reviews = 0
    text.delete('1.0', END)
    query = tf2.get()
    train = pd.read_csv(filename,encoding='utf8')
    count = 0
    total = 0
    cols = train.shape[1]
    m = 0
    n = 0
    if cols == 2:
        m = 0
        n = 1
    else:
        m = 1
        n = 16
    print(str(m)+" "+str(n))    
    for i in range(len(train)):
        name = str(train.get_value(i,m,takeable = True))
        sentence = str(train.get_value(i,n,takeable = True))
        if query in name:
            total = total + 1
            sentiment_dict = sid.polarity_scores(sentence)
            compound = sentiment_dict['compound']
            negative = sentiment_dict['neg']
            if compound <= - 0.05 :
                text.insert(END,str(sentence.encode('UTF-8'))+" == "+str(negative)+"\n")
                count = count + 1
    negative_reviews = count            
    negative_mean = count / total            
    text.insert(END,"\n\nTotal Reviews    : "+str(total)+"\n")
    text.insert(END,"Negative Reviews     : "+str(count)+"\n\n\n")
    text.see(END)
    
def productScore():
    text.delete('1.0', END)
    text.insert(END,"Mean Positivity : "+str(positive_mean)+"\n\n")
    text.insert(END,"Mean Negativity : "+str(negative_mean)+"\n\n")

def graph():
    height = [positive_reviews,negative_reviews]
    bars = ('Total Positive Reviews', 'Total Negative Reviews')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()
    
font = ('times', 15, 'bold')
title = Label(main, text='OPINION MINING FOR FEEDBACK MANAGEMENT SYSTEM')
title.config(bg='mint cream', fg='olive drab')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
ff = ('times', 12, 'bold')

l1 = Label(main, text='Enter A Comment:')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=40)
tf1.config(font=font1)
tf1.place(x=230,y=100)

runButton = Button(main, text="Run", command=module1)
runButton.place(x=330,y=150)
runButton.config(font=ff)

l2 = Label(main, text='Upload Dataset:')
l2.config(font=font1)
l2.place(x=50,y=200)

tf2 = Entry(main,width=40)
tf2.config(font=font1)
tf2.place(x=230,y=200)

uploadButton = Button(main, text="Upload", command=upload)
uploadButton.place(x=680,y=200)
uploadButton.config(font=ff)

positiveButton = Button(main, text="Positive Reviews", command=positiveReviews)
positiveButton.place(x=10,y=250)
positiveButton.config(font=ff)

negativeButton = Button(main, text="Negative Reviews", command=negativeReviews)
negativeButton.place(x=150,y=250)
negativeButton.config(font=ff)

productButton = Button(main, text="Product Score", command=productScore)
productButton.place(x=310,y=250)
productButton.config(font=ff)

graphButton = Button(main, text="Graphical Analysis", command=graph)
graphButton.place(x=450,y=250)
graphButton.config(font=ff)

font1 = ('times', 13, 'bold')
text=Text(main,height=15,width=100)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=300)
text.config(font=font1)

main.config(bg='gainsboro')
main.mainloop()
