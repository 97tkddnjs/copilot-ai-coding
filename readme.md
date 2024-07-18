# chat bot 제작

1. pip install streamlit 을 통해서 front end 문제를 쉽게 풀어나가고자 함

2. dot env 를 통해 환경 변수를 hidden 하고자 함
https://daco2020.tistory.com/480


## issue


pyspyder 가 없었음 설치를 통해서 해결함

1. $ pip install spyder==5.1.5

https://wide-shallow.tistory.com/24


axios 403 error

streamlit run main.py --server.enableXsrfProtection false

https://discuss.streamlit.io/t/file-upload-fails-with-error-request-failed-with-status-code-403/27143/61




##  공부 하면서 참고한 곳

백터 DB 관련!

https://velog.io/@jinman-kim/VectorDB-%EB%B2%A1%ED%84%B0-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4-%EA%B0%9C%EB%85%90

SentenceTransformer 알고리즘을 설명 국문

https://heeya-stupidbutstudying.tistory.com/entry/DL-SBERTSentence-BERT-sentence-embedding


## 추후 참고하면 좋을 곳

- 자연어 처리 관련 입문

https://wikidocs.net/book/2155

- LLM 관련 

https://devocean.sk.com//blog/techBoardDetail.do?ID=166285



# embeding_chat.py 아키텍처

 +---------------------------------+
 |           사용자 인터페이스          |
 |         (Streamlit 앱)           |
 |                                 |
 | 1. PDF 업로드 및 질문 입력         |
 |                                 |
 +---------------+-----------------+
                 |
                 v
 +---------------+-----------------+
 |           PDF 처리 및 임베딩        |
 |  (PyMuPDF/pdfplumber,          |
 |   Sentence-Transformers)       |
 |                                 |
 | 2. PDF에서 텍스트 추출             |
 | 3. 텍스트 임베딩 생성              |
 |                                 |
 +---------------+-----------------+
                 |
                 v
 +---------------+-----------------+
 |              벡터 검색              |
 |        (Faiss 라이브러리)           |
 |                                 |
 | 4. 질문 임베딩 생성                |
 | 5. 질문과 가장 유사한 텍스트 검색    |
 |                                 |
 +---------------+-----------------+
                 |
                 v
 +---------------+-----------------+
 |       질문 응답 생성 (LLM)        |
 |         (OpenAI API)            |
 |                                 |
 | 6. 검색된 텍스트 기반으로 질문 전달    |
 | 7. LLM을 통해 답변 생성             |
 |                                 |
 +---------------+-----------------+
                 |
                 v
 +---------------+-----------------+
 |          사용자 인터페이스           |
 |       (Streamlit 앱)               |
 |                                 |
 | 8. 답변 출력                       |
 |                                 |
 +---------------------------------+