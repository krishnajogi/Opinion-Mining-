from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

sid = SentimentIntensityAnalyzer()

def getCount(sentence):
    pos = []
    neg = []
    neu = []
    arr = sentence.split(' ')
    for i in range(len(arr)):
        word = arr[i].strip()
        if (sid.polarity_scores(word)['compound']) >= 0.3:
            pos.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.5:
            neg.append(word)
        else:
            neu.append(word)
    return pos,neg,neu        

def detectSentiment(sentence):
    sentiment_dict = sid.polarity_scores(sentence)
    negative = sentiment_dict['neg']
    positive = sentiment_dict['pos']
    neutral = sentiment_dict['neu']
    compound = sentiment_dict['compound']
    print("Positive : "+str(positive))
    print("Negative : "+str(negative))
    print("Neutral : "+str(neutral))
    print("Compound : "+str(compound))
    result = ''
    '''
    if positive > negative and positive > neutral:
        result = 'Positive'
    elif negative > positive and negative > neutral:
        result = 'Negative'
    elif neutral > positive and neutral > negative:
        reuslt = 'Neutral'
    '''
    if compound >= 0.05 : 
        result = 'Positive' 
  
    elif compound <= - 0.05 : 
        result = 'Negative' 
  
    else : 
        result = 'Neutral'
    pos,neg,neu = getCount(sentence)
    print(str(pos)+" == "+str(neg)+" == "+str(neu))
    print(result+"\n\n")    


detectSentiment('The cmr is a very good college')
train = pd.read_csv('input.txt',encoding='utf8')
for i in range(len(train)):
    sentiment = train.get_value(i,0,takeable = True)
    detectSentiment(sentiment)
