# import libararies

import re
import string
import unicodedata
import nltk
from nltk import ngrams
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

stop_words = list(stopwords.words('english'))


# define functions 

def lowercase(text):
    """
    Input:
    text (string)
    
    Returns:
    Lowercased text string
    """
    return text.lower()


def strip_accents(text):
    """
    Input:
    text (string)
    
    Returns:
    text (string): Text without accents
    """
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass

    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")

    return str(text)


def strip_punctuation(text):
    """
    Input:
    text (string)
    
    Returns:
    Text string without punctuation
    """
    return text.rstrip().translate(str.maketrans('', '', string.punctuation))

    
def strip_url(text):  
    """
    Input:
    text (string)
    
    Returns:
    Text string without url
    """
    return re.sub(r"http\S+", '', text)
    

def tokenise(text):
    """
    Input:
    text (string)
    
    Returns:
    A list of tokens
    """
    return text.split()


def strip_alpha_numeric_characters(tokens):
    """
    Input:
    tokens (list)
    
    Returns:
    A list of tokens without alpha numeric characters
    """
    
    return [token for token in tokens if token.isalpha()]        


def strip_stopwords(tokens, stopwords):
    """
    Input:
    tokens (list)
    stopwords (list)
    
    Returns:
    A list of tokens without stopwords
    """
    return list(set(tokens) - set(stop_words))        


def lemantization(tokens):
    """
    Input:
    tokens (list)
    
    Returns:
    A list of lemantized tokens
    """
    return [WordNetLemmatizer().lemmatize(token) for token in tokens]
 
    
def stemming(tokens):
    """
    Input:
    tokens (list)

    Returns:
    A list of stemmed tokens. The Porter Stemming algorithm is used. 
    """
    return [PorterStemmer().stem(token) for token in tokens]   

  
def get_ngrams(text, n_grams):
    """
    Parameters:
    text (string): A string of text
    n_grams (tuple): Specifies the number of ngrams e.g. (1,2) would be unigrams
                     and bigrams, (1,1) would be unigrams.
                     
    Returns:
    ngrams_list(list): A list of the ngrams
    """
    ngrams_list = []
    for n in range(n_grams[0], n_grams[1]+1):
        if n <= 1:
            pass
        else:
            sentances = sent_tokenize(text)
            for sent in sentances:
                grams = ngrams(sent.split(), n)
                for gram in grams:
                    ngrams_list.append(gram)

    return ngrams_list


def preprocess(text, n_grams=(1, 1), remove_accents=False, lower=False, remove_less_than=0,
               remove_more_than=20, remove_punct=False, remove_alpha=False, remove_stopwords=False,
               remove_custom_stopwords=[], lemma=False, stem=False, remove_url=False):
    """Preprocesses text into a list of cleaned tokens.
    
    Input:
    text (string): A string of text
    n_grams (tuple): Specifies the number of ngrams e.g. (1,2) would be unigrams and bigrams,
                     (1,1) would be unigrams
    remove_accents (boolean): Removes accents
    lower (boolean): Lowercases text
    remove_less_than (int): Removes words less than X letters
    remove_more_than (int): Removes words more than X letters
    remove_punct (boolean): Removes punctuation
    remove_alpha (boolean): Removes non-alphabetic tokens
    remove_stopwords (boolean): Removes stopwords
    remove_custom_stopwords (list): Removes custom stopwords
    lemma (boolean): Lemmantises tokens (via the Word Net Lemmantizer algorithm)
    stem (boolean): Stems tokens (via the Porter Stemming algorithm)
    
    Returns:
    tokens (list): A list of cleaned tokens
    """
        
    if lower is True:
        text = lowercase(text)

    if remove_accents is True:
        text = strip_accents(text)

    if remove_punct is True:
        text = strip_punctuation(text)

    if remove_url is True:
        text = strip_url(text)

    tokens = tokenise(text)

    if remove_alpha is True:
        tokens = strip_alpha_numeric_characters(tokens)

    if remove_stopwords is True:
        tokens = strip_stopwords(tokens, stop_words)

    if len(remove_custom_stopwords) > 0:
        tokens = strip_stopwords(tokens, remove_custom_stopwords)

    if lemma is True:
        tokens = lemantization(tokens)

    if stem is True:
        tokens = stemming(tokens)

    ngrams_list = get_ngrams(text, n_grams)

    return tokens + ngrams_list