# VoiceOfSeoul(서울특별시 민원데이터 분석 프로젝트)


## 1. 프로젝트 소개
    주관 : 서울디지털재단  
    개요 : 서울특별시 민원 텍스트 데이터 수집, 전처리, 키워드 추출, 토픽모델링 분석 연구 프로젝트.
  #### 가. 대상 데이터
  A. [민주주의 서울(舊 천만상상오아시스)](https://democracy.seoul.go.kr/front/index.do)  
        데이터 출처 : [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/datasetView.do?infId=OA-2563&srvType=S&serviceKind=1&currentPageNo=1)
            
  B. [서울특별시 응답소 內 '원순씨에게 바랍니다'](http://eungdapso.seoul.go.kr/Shr/Shr01/Shr01_lis.jsp)  
        데이터 출처 : Selenium 패키지를 활용해 직접 사이트에서 직접 수집
            
            
  #### 나. 사용언어 및 주요 패키지
        Python, Selenium, Pandas, PyKomoran(https://github.com/shineware/PyKOMORAN), Scikit-learn, Gensim, Numpy
  
  
## 2. 코드 설명
  #### 00Crawl.py
        - Selenium 패키지를 활용해 서울특별시 응답소 內 '원순씨에게 바랍니다'의 모든 민원 데이터 수집.  
        - 크롬 webdriver 파일(chromedriver.exe) 필요.
        
  #### 01Preprocessing.py
        - 00Crawl.py에서 수집한 <서울 응답소 데이터>와 민주주의서울 및 천만상상오아시스 데이터 전처리.
        - Pykomoran을 활용해 민원 텍스트에서 '명사'만 추출함.
        - 이 과정에서 민원에 최적화된 사용자 사전(User Dictionary) 구축해 정확한 형태소 분석 가능.
        - 정규표현식 활용하여 민원 텍스트 內 불필요한 html 태그 등 제거.
        
  #### 02TopicModel.py
        - 
  
  #### 03Vectorize.py

## 3. 프로젝트 참여자
- 서울디지털재단 박건철 책임(parkkc07@sdf.seoul.kr, https://github.com/SeoulDigitalFoundation)
- 성균관대 인터랙션사이언스 대학원 김병준 박사과정(kuntakim88@gmail.com, https://github.com/ByungjunKim)
- 성균관대 인터랙션사이언스 대학원 이겨레 박사과정(happyeffect@gmail.com, https://github.com/KyeoReLee)
