from snownlp import SnowNLP
from scipy.stats import linregress

def analyze_sentiment(text):
    return round(SnowNLP(text).sentiments, 4)

def calc_emotion_slope(sentiments):
    if len(sentiments) < 2:
        return 0.0
    x = list(range(len(sentiments)))
    slope, _, _, _, _ = linregress(x, sentiments)
    return round(slope, 4)

def calc_cumulative_gain(sentiments):
    gain = 0
    for i in range(1, len(sentiments)):
        delta = sentiments[i] - sentiments[i-1]
        if delta > 0:
            gain += delta
    return round(gain, 4)
