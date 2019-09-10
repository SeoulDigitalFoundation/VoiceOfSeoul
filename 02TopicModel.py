# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models.callbacks import PerplexityMetric
import os

import seaborn
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rc('font', family='Malgun Gothic')

import numpy as np
from scipy.spatial.distance import cosine
from scipy.sparse import save_npz, load_npz
from scipy.stats import linregress
from pprint import pprint

# Enable logging for gensim - optional
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

#LDAvis
import pyLDAvis
import pyLDAvis.gensim # don't skip this
import matplotlib.pyplot as plt
# %matplotlib inline


## gensim LDA용 추가 토크나이징(bigram 등) ##
#  Build the bigram and trigram models
bigram = gensim.models.Phrases(master['nouns_stopwords'].to_list(), min_count=10) # higher threshold fewer phrases.
bigram_mod = gensim.models.phrases.Phraser(bigram)

def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]
    
# Form Bigrams
data_words_bigrams = make_bigrams(master['nouns_stopwords'].to_list())
data_words_bigrams_oasis = make_bigrams(oasis_demo[oasis_demo['category']=='천상오']['nouns_stopwords'].to_list())

# Unigrams
#data_words_unigrams = master['nouns'].to_list()

# Create Dictionary
id2word = corpora.Dictionary(data_words_bigrams) #bigram
#id2word = corpora.Dictionary(data_words_unigrams) #unigram

# Create Corpus
corpus = [id2word.doc2bow(text) for text in data_words_bigrams] #bigram
#corpus = [id2word.doc2bow(text) for text in data_words_unigrams] #unigram

# View
print(corpus[:1])
id2word[0]

# Human readable format of corpus (term-frequency)
[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]

# 불필요 변수 삭제
#del data_words_bigrams, data_words_unigrams


### 전체시기 일반 LDA ###
# load #
lda_model_whole = gensim.models.ldamodel.LdaModel.load('Whole_period.model')

lda_model_whole = gensim.models.ldamodel.LdaModel(corpus=corpus,
        id2word=id2word,
        num_topics=10, #output 토픽수
        random_state=100,
        update_every=1, #모델 매개변수 업데이트 빈도
        chunksize=100, #각 훈련 chunk에서 사용할 문서 수
        passes=10, #총 훈련 과정 수
        alpha='auto',
        per_word_topics=True)

lda_model_whole.save('Whole_period.model')

# Visualize the topics
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model_whole, corpus, id2word)
# pyLDAvis.display(vis)
pyLDAvis.save_html(vis,'../03output/LDA/전체_vis.html') #save

# Compute Perplexity
print('\nPerplexity: ', lda_model_whole.log_perplexity(corpus))
 
# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model_whole, texts=data_words_bigrams, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)