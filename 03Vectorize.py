### Packages ###
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# import seaborn
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rc('font', family='Malgun Gothic')


plt.plot(master.groupby('year')['contents'].count())

### TF-IDF Vector ###
tfidf_vectorizer = TfidfVectorizer(analyzer='word',
                             lowercase=False,
                             tokenizer=None,
                             preprocessor=None,
                             min_df=5, # 최소 문서 수 5건
                             ngram_range=(1,1), #Bigram : ngram_range=(1,2)
                             smooth_idf=True
                             #max_features=10000 #메모리문제로 설정
                             )

#명사 전체
tfidf_vector = tfidf_vectorizer.fit_transform(master['nouns'].astype(str))

#정리#
tfidf_scores = tfidf_vector.toarray().sum(axis=0)
tfidf_idx = np.argsort(-tfidf_scores)
tfidf_scores = tfidf_scores[tfidf_idx]
tfidf_vocab = np.array(tfidf_vectorizer.get_feature_names())[tfidf_idx]
print(list(zip(tfidf_vocab, tfidf_scores))[:100])
tfidf_vocab

##TF-IDF 기준 Term-Term Matrix
tfidf_term_term_mat = cosine_similarity(tfidf_vector.T)
tfidf_term_term_mat = pd.DataFrame(tfidf_term_term_mat,index=tfidf_vectorizer.vocabulary_,columns=tfidf_vectorizer.vocabulary_)

# 상위 100개 단어-단어 매트릭스 추출
tfidf_term_term_mat_100 = tfidf_term_term_mat[tfidf_term_term_mat.keys().isin(tfidf_vocab[:100])]
tfidf_term_term_mat_100 = tfidf_term_term_mat_100[tfidf_term_term_mat_100.columns.intersection(tfidf_vocab[:100])]
tfidf_term_term_mat_100
