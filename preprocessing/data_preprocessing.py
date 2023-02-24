import pandas as pd
import nltk 
import string 
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter 
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer

def drop_columns(input_df: pd.DataFrame, columns:list):
    r""" Drop a list of given columns 
    Parameters
    ----------
    input_df: pd.DataFrame, input dataframe 
    columns: list, list of columns to drop

    Return 
    ------
    output_df: pd.DataFrame, output dataframe 

    """

    output_df = input_df.drop(columns, axis=1)
    return output_df


def rename_columns(input_df:pd.DataFrame, col_map:dict):
    r""" Rename a list of columns with a given mapping 
    Parameters
    ----------
    input_df: pd.DataFrame, input dataframe 
    col_map: dictionary, mapping for the columns (e.g. "colA": "spam") 
    
    Return 
    ------
    output_df: pd.DataFrame, output dataframe
    """
    output_df = input_df.rename(columns=col_map)
    return output_df 


def target_encoder(input_df: pd.DataFrame, target_a: str, target_b: str):
    r""" Convert the target columns to binary values 0/1 
    Parameters
    ----------
    input_df: pd.DataFrame, input dataframe 
    target_a: str, name of the target to be encoded to 0 
    target_b: str, name of the target to be encoded to 1
    
    Return 
    ------
    output_df: pd.DataFrame, output dataframe
    """
    output_df = input_df.replace([target_a, target_b], [0,1])
    return output_df

def text_processing(input_df):
    r""" A set of custom text processing 
    Parameters
    ----------
    input_df: pd.DataFrame, input dataframe 
    
    Return 
    ------
    """
    def remove_stopwords(input_text:str):
        r""" Given an input string remove its stopwords 
        Parameters
        ----------
        input_text: str 
        """
            
        text = input_text.translate(str.maketrans('', '', string.punctuation))
        text = [word for word in text.split() if word.lower() not in stopwords.words('english')]

        return " ".join(text)

    input_df['text'] = input_df['text'].apply(remove_stopwords)
    # convert the text to a numerical vector with TF-IDF 
    vectorizer = TfidfVectorizer() # caveat, this should be saved aside and used later in inference
    vectors = vectorizer.fit_transform(input_df['text'])

    return vectors
    
