from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings("ignore")

from sklearn.feature_extraction.text import CountVectorizer

from gensim.models.ldamulticore import LdaMulticore
from gensim.corpora import Dictionary
from gensim.matutils import corpus2csc
import numpy as np

from gensim.models import LsiModel

from sklearn.feature_extraction.text import TfidfVectorizer


class Transformer(ABC):
  def __init__(self, params):
    pass

  @abstractmethod
  def fit(self, train_vector):
    '''
    Args:
      train_vector: numpy array with pre-transformed fingerprint data (the training data)

    Returns:
      None
    '''
    pass

  @abstractmethod
  def transform(self, vector):
    '''
    Args:
      vector: numpy array with pre-transformed fingerprint data (training or testing data)

    Returns:
      transformed data
    '''
    pass

class BaseTransformer(Transformer):
  def __init__(self, params):
    self.transformer = None

  def fit(self, train_vector):
    '''
    Args:
      train_vector: numpy array with pre-transformed fingerprint data (the training data)

    Returns:
      None
    '''
    self.transformer.fit(train_vector)

  def transform(self, vector):
    '''
    Args:
      vector: numpy array with pre-transformed fingerprint data (training or testing data)

    Returns:
      transformed data
    '''
    transformed_vector = self.transformer.transform(vector).todense()
    return transformed_vector

class BagOfWords(BaseTransformer):
  def __init__(self, params):
    self.transformer = CountVectorizer(**params)

class LDA(BaseTransformer):
  def __init__(self, params):
    self.transformer = None
    self.params = params

  def fit(self, vector):
    train_corpus, id2word = self._create_corpus(vector)
    self.transformer      = LdaMulticore(train_corpus, id2word=id2word, **self.params)

  def transform(self, vector):
    corpus, id2word    = self._create_corpus(vector)

    transformed_vector = []
    for i in range(len(vector)):
      all_topics = self.transformer.get_document_topics(corpus[i], minimum_probability=0.0)
      topic_vec  = [all_topics[i][1] for i in range(len(all_topics))] ## get the topic probs from the tuple
      transformed_vector.append(topic_vec) ## add this topic vector to final vector

    transformed_vector = np.array(transformed_vector)

    return transformed_vector

  def _create_corpus(self, vector):
    vector_tokens  = np.array([x.split(' ') for x in vector.ravel()])
    id2word = Dictionary(vector_tokens)

    ## no_below - get rid of words that appear less than 10 times in the corpus of docs
    ## no_above - get rid of words that appear more than 35% of the time in the corpus of docs
    id2word.filter_extremes(no_below=10, no_above=0.35)
    id2word.compactify()
    corpus = [id2word.doc2bow(text) for text in vector_tokens] ### BOW representation of the words

    return corpus, id2word

class LSI(BaseTransformer):
  def __init__(self, params):
    self.transformer = None
    self.params = params

  def fit(self, vector):
    train_corpus, id2word = self._create_corpus(vector)
    self.transformer      = LsiModel(train_corpus, id2word=id2word, **self.params)

  def transform(self, vector):
    corpus, id2word    = self._create_corpus(vector)
    transformed_corpus = self.transformer[corpus]
    all_topics_csr     = corpus2csc(transformed_corpus)
    transformed_vector = all_topics_csr.T.toarray()

    return transformed_vector

  def _create_corpus(self, vector):
    vector_tokens  = np.array([x.split(' ') for x in vector.ravel()])
    id2word = Dictionary(vector_tokens)

    ## no_below - get rid of words that appear less than 10 times in the corpus of docs
    ## no_above - get rid of words that appear more than 35% of the time in the corpus of docs
    id2word.filter_extremes(no_below=10, no_above=0.35)
    id2word.compactify()
    corpus = [id2word.doc2bow(text) for text in vector_tokens] ### BOW representation of the words

    return corpus, id2word

class TFIDF(BaseTransformer):
  def __init__(self, params):
    self.transformer = TfidfVectorizer(**params)
