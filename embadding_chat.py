import streamlit as st

import fitz  # 또는 pdfplumber
from sentence_transformers import SentenceTransformer
import faiss


# Streamlit 설정
st.title("AI RAG 프로젝트")
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")


# PDF 파일을 읽어 텍스트로 변환하는 함수
def read_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text



def save_sentences_to_txt(sentences, filename="sentences.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence.strip() + "\n")


if uploaded_file is not None:

    text =  read_pdf(uploaded_file)
    
    print(text)
    data = []
    data = text.split('.') # 문장 단위로 분리
    print(data)

    # txt 파일로 저장
    save_sentences_to_txt(data)

    # 텍스트 임베딩 생성
    model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
    embeddings = model.encode(data) # 문장 임베딩 생성
    
    print('debugging ')
    print(embeddings.shape) # shape 는 (문장 수, 임베딩 차원)


    
    # Faiss 인덱스 생성 및 임베딩 추가 ,  L2 거리는 유클리드 거리를 의미하며, 벡터 간의 직선 거리를 계산
    index = faiss.IndexFlatL2(embeddings.shape[1]) # 임베딩 차원과 동일한 차원으로 인덱스 생성
    index.add(embeddings)   # 임베딩 추가

    # 질문 입력
    question = st.text_input("질문을 입력하세요")

    if question:
        # 질문 임베딩 생성
        question_embedding = model.encode([question])
        context =[]
        # 질문과 가장 유사한 텍스트 검색
        D, IDXS = index.search(question_embedding, k=10)
        print('debugging', D, IDXS )
        for IDX in IDXS[0]:
            tmp = data[IDX]
            print(data[IDX])
            context.append(tmp)
        
        

        st.write(context)
        # LLM에 질문 전달 및 답변 생성
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=f"Context: {context}\n\nQuestion: {question}\n\nAnswer:",
        #     max_tokens=150
        # )
        
        # # 답변 출력
        # st.write(response.choices[0].text.strip())

    