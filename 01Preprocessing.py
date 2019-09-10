### Load packages ###
from PyKomoran import *
komoran = Komoran("STABLE")
komoran.set_user_dic("dic.txt") #기존 천만상상 오아시스 사전 변형 활용

import pandas as pd
import pickle
import regex
import re
from tqdm import tqdm
tqdm.pandas()

# import seaborn
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rc('font', family='Malgun Gothic')


### 1. Data table ###
##민주주의 서울##
demo_free = pd.read_excel(r"190831_민주주의 서울 자유제안 정보.xls")
demo_free.columns
demo_free.제안제목[0]
demo_free.제안내용[0]

#민주주의 서울 오픈일 : 17.10.24
demo_assigned = pd.read_excel(r"190715_민주주의 서울 채택제안 정보.xls")
demo_assigned.columns

# merge 자유 + 채택 #
demo_free[['제안번호','제안제목','제안내용','제안등록일자']]
demo_assigned[['제안번호','제안제목','제안내용','제안등록일자']]

demo = pd.concat([demo_free[['제안번호','제안제목','제안내용','제안등록일자']],
demo_assigned[['제안번호','제안제목','제안내용','제안등록일자']]],ignore_index=True)
del demo_free, demo_assigned

demo.dropna(subset=['제안내용'], inplace=True) #제안 내용 없는 row 삭제

print('combine title and text')
demo['contents'] = demo.apply(lambda x:x['제안제목']+"\n"+x['제안내용'],axis=1)
demo.drop_duplicates(subset='contents',inplace=True) #제목 + 내용 중복 row 삭제

demo.sort_values(by='제안번호',inplace=True)
demo.reset_index(inplace=True,drop=True)

#html tag 내 한글 제거
def remove_tag(content):
    cleaner = re.compile('<.*?>')
    cleantext = re.sub(cleaner,'',content)
    return cleantext

tag_pattern = regex.compile(r'class\=\"*\p{Hangul}+\"*|font-family\: \"*\p{Hangul}+\"*|HY중고딕|서울남산체|맑은 고딕|함초롬바탕|굴림|굴림체|새굴림|고딕|나눔고딕|산돌고딕|모던고딕|한양중고딕|HY견명조|바탕|태그래픽|궁서|궁서체|휴먼 명조|휴먼명조')
regex.sub(tag_pattern,'','font-family: "맑은 고딕; mso-ascii-font-family: HY중고딕;')

print('delete tags')
demo['contents'] = demo['contents'].map(lambda x:remove_tag(x))
demo['contents'] = demo['contents'].map(lambda x:regex.sub(tag_pattern,'',x))


# 제안등록일자 date 변수화 #
demo['제안등록일자'] = pd.to_datetime(demo['제안등록일자'],infer_datetime_format=True)
demo['제안등록일자'][0].year

demo['year'] = demo['제안등록일자'].map(lambda x:x.year)

# 민주주의 서울 內 천상오 데이터 분리
#demo = demo[demo['제안등록일자']>='2017-10-24 00:00:00'] #2017년 10월 24일 이후 데이터만 활용
demo['category'] = '민주주의서울'
demo['category'][demo['제안등록일자']>='2017-10-24 00:00:00'] = '민주주의서울'
demo['category'][demo['제안등록일자']<'2017-10-24 00:00:00'] = '천상오'


## 서울 응답소 ##
response = pd.read_csv(r"190809_서울응답소.csv")
response.dropna(subset=['contents'], inplace=True) #제안 내용 없는 row 삭제
response.rename(columns={'title':'제안제목','contents':'제안내용','answer':'답변내용'},inplace=True)

print('combine title and text')
response['제안내용'] = response.apply(lambda x:x['제안제목']+"\n"+x['제안내용'],axis=1)
response['제안내용'] = response['제안내용'].map(lambda x:re.sub(r'Q. 상담내용\n','',x)) #상담내용 문구 제거


# 제안등록일자 date 변수화 #
response.rename(columns={'date':'제안등록일자'},inplace=True)
response.columns
response['제안등록일자'] = pd.to_datetime(response['제안등록일자'],infer_datetime_format=True)
response['제안등록일자'][0].year

response.sort_values(by='제안등록일자',inplace=True)

#response = response[response['제안등록일자']>='2017-10-24 00:00:00'] #2017년 10월 24일 이후 데이터만 활용
response = response[response['제안등록일자']>='2015-01-01 00:00:00'] #2015년 이후 데이터만 활용
response.reset_index(inplace=True,drop=True)

response['contents'] = response.apply(lambda x:x['제안제목']+"\n"+x['제안내용'],axis=1)
response['category'] = '응답소'


## 천상오 ##
oasis = pd.read_csv(r'G:\공유 드라이브\democracy_seoul\01data\03천상오\천상오.csv',sep="\t")
oasis.rename(columns={'제목':'제안제목','내용':'제안내용','작성일':'제안등록일자'},inplace=True)

oasis.dropna(subset=['제안제목','제안내용'],inplace=True)

oasis['제안등록일자'] = pd.to_datetime(oasis['제안등록일자'],infer_datetime_format=True)
oasis = oasis[oasis['제안등록일자']>='2016-01-01 00:00:00'] # 2016년 이후 데이터만 활용
# oasis = oasis[oasis['제안등록일자']>='2015-01-01 00:00:00'] # 2015년 이후 데이터만 활용

oasis.reset_index(inplace=True,drop=True)

oasis['contents'] = oasis.apply(lambda x:x['제안제목']+"\n"+x['제안내용'],axis=1)
oasis['category'] = '천상오'



## master = 민주주의서울+서울응답소+천상오 ##
common_list = ['제안제목', '제안내용', '제안등록일자', 'contents', 'category']

demo[common_list]
response[common_list]
oasis[common_list]


### Merge ###
master = pd.concat([demo[common_list],response[common_list],oasis[common_list]],ignore_index=True)

master['year'] = master['제안등록일자'].dt.year

#민주주의서울 內 천상오 데이터는 2015년 이후만 활용
master = master[(master['제안등록일자']>='2015-01-01 00:00:00')]

#제목 &  제안내용 중복 삭제
master.drop_duplicates(subset=['제안제목','제안내용'], inplace = True)
#contents 중복내용 삭제
master.drop_duplicates(subset=['contents'], inplace = True)
master.sort_values('제안등록일자',inplace=True) #날짜순으로 정렬
master.reset_index(drop=True,inplace=True)

### 2. 토크나이징 ###
#특수문자 제거#
def cleanText(readData):
    #텍스트에 포함되어 있는 특수 문자 제거, 공백제거
    #text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》\’\“\”\·\n\r\t■◇◆▶;]', '', readData).strip()
    return text

# 형태소 분석 #
# 포함할 형태소 : SL(외국어), NNG(일반명사), NNP(고유명사), VA(형용사), VV(동사), MAG(일반부사)
# VA(형용사)와 VV(동사)는 종결어미 '다' 추가
def morp(strings):
   return [w.get_first()+'다' if w.get_second() in ['VV','VA'] else w.get_first() for w in komoran.get_list(cleanText(strings)) if w.get_second() in ['NNP','NNG','MAG','VA','VV']]

# demo['tokens'] = demo['contents'].progress_mapy(lambda x:morp(x))
# demo['tokens'] = demo_dd.map(lambda x:morp(x)).compute()
# del demo_dd

print('토크나이징 시작')
# master['tokens'] = master['contents'].map(lambda x:morp(x))
master['nouns'] = master['contents'].progress_map(lambda x:komoran.get_nouns(cleanText(x)))

## 불용어 제거 ##
stopwords = ['아래', '상상', '제안', '까지', '닷컴', '포털', '사이트', '천만', '오아시스', '이벤트', '접수','서울시','서울','특별시',
             '천만상상','파일','첨부','응모','슬로건','공모','공모전','응모전','신청','경우','때문','정도','사항',
                   '해당','겁니다','이것','저것','그것','돋움','신명', '태명', '한컴', '돋움',
                   '동안','거기','저기','여기','대부분','누구','무엇','고딕','만큼','굴림','감사','건지','텐데',
                   '안녕','이번','걸로','수고','겁니까','그간','그건','그때','글쓴이','누가','니다','다면',
                   '뭔가','상상오아시스','하다','이다','되다','같다','궁','자체','서체','정','서','이','을','있다','없다', '체','관련',
                   '생각', '현재', '진행', '사람', '마음', '남산', '내용', '현실','음','막','김','변','조',
                   '오','참','동','지금','주변','대상','부분','요즘','하루','마련','세대','시간','이상','행위',
                   '활동','구분','사실','과정','모습','기간','선정','단지','자신','발생','지역','기대','마련',
                   '장소','모두','부탁','제공','이용','해주','당시','최근','민원','문제','문제점','현황','개선','방안',
                   '문의','답변','일동','요청','담당자','직원','방법','사용','활용','확인','방식','예전']
stopwords.append('제가')
stopwords.append('홈페이지')
stopwords.append('오시')
# stopwords.append('글')
# stopwords.append('윤')
# stopwords.append('다')
# stopwords.append('때')
# stopwords.append('한')
# stopwords.append('안')
stopwords_set = set(stopwords)

# 한글자 제거 #
hangul_1 = regex.compile(r'^\p{Hangul}{1}$')
# 명사 토크나이징 #
master['nouns_stopwords'] = master['nouns'].map(lambda x:[w for w in x if not w in stopwords_set if not hangul_1.match(w)])