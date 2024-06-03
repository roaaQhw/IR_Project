import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import contractions
import re
from nltk.stem import PorterStemmer
import inflect
import pandas as pd

import nltk

# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

# Load stopwords from NLTK


# app = Flask(__name__)


nltk_stop_words = set(stopwords.words('english'))
custom_stop_words = set([
    'some', 'where', 'also', 'after', 'often', 'about', 'above', 'across', 'afterwards',
    'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'although', 
    'always', 'among', 'amongst', 'amount', 'another', 'anyhow', 'anyone', 'anything',
    'anyway', 'anywhere', 'around', 'back', 'before', 'behind', 'below', 'beside', 
    'besides', 'between', 'beyond', 'both', 'bottom', 'but', 'call', 'can', 'cannot',
    'describe', 'detail', 'down', 'due', 'during', 'each', 'either',
    'else', 'elsewhere', 'empty', 'enough', 'even', 'ever', 'every', 
    'everyone', 'everything', 'everywhere', 'few', 'former', 'formerly', 
    'found', 'front', 'full', 'further',
    'give', 'has', 'hence', 'here', 'hitherto', 'how', 'however', 'indeed',
    'inside', 'instead', 'into', 'itself', 'just', 'keep', 'last', 'latter', 'latterly',
    'least', 'less', 'made', 'many', 'may', 'meanwhile', 'might', 'more', 'moreover', 
    'most', 'mostly', 'move', 'much', 'must', 'myself', 'name', 'namely', 'neither',
    'never', 'nevertheless', 'next', 'nobody', 'none', 'noone', 'nothing', 
    'now', 'nowhere', 'only', 'onto', 'others', 'otherwise',
    'ourselves', 'out', 'over', 'part', 'per', 'perhaps', 'please', 'quite', 'rather',
    'really', 'regarding', 'same', 'seem', 'seemed', 'seeming', 'seems', 'several',
    'she', 'should', 'show', 'side', 'since', 'somehow', 'someone',
    'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'take', 
    'thence', 'therefore', 'thereafter', 'thereby', 'therefore', 'therein',
    'thereupon', 'these', 'they', 'third', 'this', 'those', 'though',  
    'through', 'throughout', 'together', 'too', 'top', 'toward', 'towards', 
    'under', 'unless', 'upon', 'various', 'very', 'via', 'was', 'well', 
    'whatever', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 
    'wherever', 'whether', 'whither', 'whole', 'whose', 'why', 'will', 'with', 
    'within', 'without', 'would', 'yet'
])

all_stop_words = nltk_stop_words.union(custom_stop_words)
abbreviations = {
    'Dr.': 'Doctor',
    'Mr.': 'Mister',
    'Mrs.': 'Misess',
    'Ms.': 'Misess',
    'Jr.': 'Junior',
    'Sr.': 'Senior',
    'U.S': 'UNITED STATES',
    'U-S': 'UNITED STATES',
    'U_K': 'UNITED KINGDOM',
    'U_S': 'UNITED STATES',
    'U.K': 'UNITED KINGDOM',
    'U.S': 'UNITED STATES',
    'VIETNAM': 'VIET NAM',
    'VIET NAM': 'VIET NAM',
    'U-N': 'NITED NATIONS',
    'U_N': 'NITED NATIONS',
    'U.N': 'NITED NATIONS',
    'UK': 'UNITED KINGDOM',
    'US': 'UNITED STATES',
    'U-K': 'UNITED KINGDOM',
    'mar': 'March',
    'march': 'March',
    'jan': 'January',
    'anuary': 'January',
    'feb': 'February',
    'february': 'February',
    'apr': 'April',
    'april': 'April',
    'jun': 'June',
    'june': 'June',
    'jul': 'July',
    'july': 'July',
    'dec': 'December',
    'december': 'December',
    'nov': 'November',
    'november': 'November',
    'oct': 'October',
    'october': 'October',
    'sep': 'September',
    'september': 'September',
    'aug': 'August',
    'august': 'August',
}
# Function to convert text to lowercase
def to_lowercase(text):
    if isinstance(text, str):
        return text.lower()
    else:
        return str(text).lower()

def number_to_words(string):
    p = inflect.engine()
    words = string.split()
    filtered_words = []
    
    for word in words:
        if word.isdigit():
            try:
                num = int(word)
                if num < 3000:
                    # Convert the number to words
                    word_as_words = p.number_to_words(word)
                    # Replace the number with its word representation
                    filtered_words.append(word_as_words)
                # If number is greater than or equal to 3000, skip it
            except ValueError:
                # If conversion to int fails, skip the word
                continue
        else:
            # Add non-numeric words to the result
            filtered_words.append(word)
    
    converted_string = ' '.join(filtered_words)
    return converted_string

# Function to expand contractions
def expand_contractions(text):
    return contractions.fix(text)

def replace_abbreviations(text):
    for abbr, full_form in abbreviations.items():
        pattern = re.compile(r'\b' + re.escape(abbr) + r'\b')
        text = pattern.sub(full_form, text)
    return text


def remove_stopwords_and_punctuation_marks(text):
    pattern = re.compile(f'[{re.escape(string.punctuation)}]')
    tokens = word_tokenize(str(text))
    
    # Remove punctuation
    tokens = [pattern.sub('', word) for word in tokens]
    
    # Filter out stopwords
    filtered_tokens = [word for word in tokens if word.lower() not in all_stop_words]
    
    return ' '.join(filtered_tokens)

# Function to get the WordNet POS tag
def get_wordnet_pos(tag):
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag[0].upper(), wordnet.NOUN)

# Function to lemmatize text
def lemmatize_text(text):
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags]
    return ' '.join(lemmatized_words)

def stem_text(text):
    porter = PorterStemmer()
    words = word_tokenize(text)
    stemmed_words = [porter.stem(word) for word in words]
    return ' '.join(stemmed_words)

def remove_urls(text):
    url_pattern = re.compile(r'http\S+|www\S+|https\S+')
    return url_pattern.sub(r'', text)


def process_text(text):
    text = remove_urls(text)
    text = replace_abbreviations(text)  
    text = to_lowercase(text)
    text = expand_contractions(text)
    text = remove_stopwords_and_punctuation_marks(text)
    text = number_to_words(text)
    text = stem_text(text)
    text = lemmatize_text(text)
    text = remove_stopwords_and_punctuation_marks(text)
    return text
