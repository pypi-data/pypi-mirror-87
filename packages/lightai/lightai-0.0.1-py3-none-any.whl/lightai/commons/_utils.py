from wordcloud import WordCloud, STOPWORDS
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
from PIL import Image


def create_word_cloud(words_list:str):
    word_freq = [words_list.count(p) for p in words_list]
    word_dict = dict(list(zip(words_list, word_freq)))
    cloud = WordCloud()
    cloud.generate_from_frequencies(frequencies=word_dict)
    return cloud

def clean_input(txt:str):
    updated_text = txt
    updated_text = updated_text.replace('<br /><br />', ' ')
    updated_text = updated_text.replace('<br />', ' ')
    tokens = word_tokenize(updated_text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return words
