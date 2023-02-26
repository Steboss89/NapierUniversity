import pandas as pd
import nltk 
import string 
from nltk.corpus import stopwords
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
from apache_beam import DoFn



class TextProcessing(DoFn):

    def process(self, element, *args, **kwargs):
        r""" Given an element perform the text cleaning
        """
        text = str(element).translate(str.maketrans('', '', string.punctuation))
        text = [word for word in text.split() if word.lower() not in stopwords.words('english')]
        processed_text =  " ".join(text)
        # theoretically this is wrong, we should have a saved TfIdF 
        vectorizer = TfidfVectorizer() 
        vectors = vectorizer.fit_transform([processed_text])

        yield vectors
        