import streamlit as st
from streamlit_chat import message
import requests
import os
from dotenv import load_dotenv
import json
import time
import fitz  # PyMuPDF

load_dotenv()

# message('My Message')
# message('hi i am sk',is_user=True)

# session state <- 페이지를 넘나 들더라도 유지하는 변수 느낌

# PDF 파일을 읽어 텍스트로 변환하는 함수
def read_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text



# 
st.header('Chatbot')

'''
변수에 있는 지 여부 밑에 if 문은 체크하는 것으로 보임

'''
if 'generated_responses' not in st.session_state:
    st.session_state['generated_responses'] = []

if 'user_inputs' not in st.session_state:
    st.session_state['user_inputs'] = []

if 'api_url' not in st.session_state:
    st.session_state['api_url'] = ''

if 'api_token' not in st.session_state:
    st.session_state['api_token'] = ''


# API url 입력 받는 인풋 창 <- 디폴트로 고정 시켜 버리기~

st.session_state['api_url'] = 'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'

# st.text_input('API_URL: ', st.session_state['api_url'])

# https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill

# api 토큰을 입력받는 인풋 창
st.session_state['api_token'] = os.getenv("API_TOKEN_KEY")
# st.text_input('API_TOKEN: ', st.session_state['api_token'], type='password')




# make code to read pdf file and save it to a variable and then read pdf file contents
# pdf file upload
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
if uploaded_file is not None:
    pass

# pdf file contents
pdf_contents = "No PDF file uploaded yet."

# 업로드된 파일이 있으면 내용을 읽어서 pdf_contents에 저장
if uploaded_file is not None:
    pdf_contents = read_pdf(uploaded_file)


# PDF 파일 내용을 텍스트 영역에 표시
st.text_area('PDF Contents', pdf_contents, height=400)



def query(payload):
    data = json.dumps(payload)

    # 토큰은 bearer 인듯
    headers = {'Authorization': f'Bearer {st.session_state.api_token}'}
    while True:
        try: 
            response = requests.post(st.session_state.api_url, headers=headers, json=data)
            # Check if the model is loading
            response.raise_for_status()
            result = response.json()
            print('result', result)
            
            if 'error' in result and 'loading' in result['error']:
                        st.warning(f"Model is loading, estimated time: {result.get('estimated_time', 'unknown')} seconds")
                        time.sleep(5)  # Wait for 5 seconds before trying again
            else:
                return result
        
        except requests.exceptions.HTTPError as e:
                st.error(f"HTTP error occurred: {str(e)}")
                st.error(f"Response content: {response.content}")
                break
        
        except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                break
    return {}
    

with st.form('form', clear_on_submit = True):
    user_input = st.text_input('Message: ', '')
    submitted = st.form_submit_button('Send')

if submitted and user_input:
    print( '====== input_param  ',st.session_state.user_inputs ,st.session_state.generated_responses  ,user_input  )
    output = query({
        'inputs': {
            'past_user_inputs': st.session_state.user_inputs,
            'generated_responses': st.session_state.generated_responses,
            'text': user_input,
        },
        # 'parameters': {'repetition_penalty': 1.33},
        'wait_for_model': True

    })

    print("=====   output ",  output, '\n')

    st.session_state.user_inputs.append(user_input)
    st.session_state.generated_responses.append(output['generated_text'] if type(output) == dict else  output[0]['generated_text'])

if st.session_state['generated_responses']:
    for i in range(0, len(st.session_state['generated_responses']), 1):
        message(st.session_state['user_inputs'][i], is_user = True)
        message(st.session_state['generated_responses'][i])