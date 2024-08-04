import streamlit as st
import fitz  # 또는 pdfplumber
import torch
# from transformers import BertTokenizer, BertModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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

# KoBERT 모델과 토크나이저 로드
# model_name = 'skt/kobert-base-v1'/
model_name = 'monologg/kobert'
tokenizer = AutoTokenizer.from_pretrained("skt/kogpt2-base-v2")

# 패딩 전략 설정
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


model = AutoModelForCausalLM.from_pretrained("skt/kogpt2-base-v2")

# 문장을 토큰화하고 텐서로 변환
def get_embeddings(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

# 문장을 정규화하는 함수
def normalize(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

# 문장을 txt 파일로 저장하는 함수
def save_sentences_to_txt(sentences, filename="sentences.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence.strip() + "\n")

if uploaded_file is not None:
    text = read_pdf(uploaded_file)
    
    data = text.split('.')  # 문장 단위로 분리
    
    # txt 파일로 저장
    save_sentences_to_txt(data)
    
    # 문장 임베딩 생성 및 정규화
    embeddings = np.array([get_embeddings(sentence) for sentence in data])
    normalized_embeddings = normalize(embeddings)
    print('임베딩 생성 완료')
    print(normalized_embeddings)
    print(normalized_embeddings.shape)
    # FAISS 인덱스 생성 및 임베딩 추가 (코사인 유사도)
    
    # 중간 차원 제거
    normalized_embeddings = np.squeeze(normalized_embeddings, axis=1)
    dimension = normalized_embeddings.shape[1]
    
    index = faiss.IndexFlatIP(dimension)  # 내적을 사용하여 코사인 유사도 계산
    index.add(normalized_embeddings)
    
    # 질문 입력
    question = st.text_input("질문을 입력하세요")
    
    if question:
        # 질문 임베딩 생성 및 정규화
        question_embedding = get_embeddings(question)
        normalized_question_embedding = normalize(np.array([question_embedding]))
        print('질문 임베딩 생성 완료')
        print(normalized_question_embedding)
        print(normalized_question_embedding.shape)
         # 중간 차원 제거
        normalized_question_embedding = np.squeeze(normalized_question_embedding, axis=1)
        # 질문과 가장 유사한 텍스트 검색
        D, IDXS = index.search(normalized_question_embedding, k=10)
        
        context = []
        for IDX in IDXS[0]:
            tmp = data[IDX]
            context.append(tmp)
        
        st.write(context)

        # LLM에 질문 전달 및 답변 생성 (옵션)
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=f"Context: {context}\n\nQuestion: {question}\n\nAnswer:",
        #     max_tokens=150
        # )
        # st.write(response.choices[0].text.strip())