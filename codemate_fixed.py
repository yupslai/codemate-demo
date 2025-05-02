import streamlit as st
import json
import random
import time
from datetime import datetime

# 로고 URL 설정 (로컬 파일 대신 URL 사용)
LOGO_URL = "https://raw.githubusercontent.com/openai/openai-python/main/assets/logo.png"

# Simulated user data
SAMPLE_USER = {
    "id": "user123",
    "name": "민호",
    "age": 11,
    "grade": 5,
    "interests": ["게임", "마인크래프트", "로봇"],
    "created_at": "2023-09-01T10:00:00"
}

# Simulated learning history
LEARNING_HISTORY = {
    "concepts": [
        {"id": "var001", "name": "변수", "understanding_level": 4, "last_practiced": "2023-09-15"},
        {"id": "loop001", "name": "반복문", "understanding_level": 2, "last_practiced": "2023-09-20"},
        {"id": "cond001", "name": "조건문", "understanding_level": 3, "last_practiced": "2023-09-18"},
        {"id": "fun001", "name": "함수", "understanding_level": 1, "last_practiced": "2023-09-22"}
    ]
}

# Sample questions and answers for demonstration
SAMPLE_QA = {
    "while_loop": {
        "question": "while 반복문이 뭐야? 마인크래프트에서 어떻게 쓸 수 있어?",
        "answer": """
안녕 민호! while 반복문은 어떤 조건이 참인 동안 계속해서 코드를 반복해서 실행하는 방법이야.

마인크래프트에서 사용하는 예를 들어볼게:

```python
# 10개의 블록을 자동으로 놓는 코드
blocks_placed = 0
while blocks_placed < 10:
    place_block()  # 블록 놓기
    move_forward() # 앞으로 이동
    blocks_placed = blocks_placed + 1
    print(f"{blocks_placed}번째 블록을 놓았어요!")
```

이 코드는 블록을 10개 놓을 때까지 반복해서 실행돼. `blocks_placed < 10`이라는 조건이 참인 동안에만 실행되고, 10개를 모두 놓으면 멈추게 돼.

마인크래프트에서 이런 반복문을 사용하면 성벽이나 다리 같은 것을 자동으로 만들 수 있어서 정말 편리하지!

더 궁금한 점이 있니?
        """
    },
    "debugging": {
        "question": "이 코드가 왜 안 되는지 모르겠어요: for i in range(10) print(i)",
        "answer": """
안녕 민호! 그 코드에는 작은 문법 오류가 있어.

Python에서 `for` 반복문 다음에 반복할 코드 블록을 시작할 때 콜론(`:`)이 필요해.

이렇게 수정해보자:

```python
for i in range(10):
    print(i)
```

콜론(`:`)을 추가하고 그 다음 줄에 들여쓰기를 했어. Python에서는 들여쓰기가 코드 블록을 구분하는 중요한 방법이야.

이렇게 하면 0부터 9까지 숫자가 출력될 거야. 한번 실행해볼래?
        """
    },
    "function": {
        "question": "함수가 뭐에요? 잘 이해가 안돼요.",
        "answer": """
안녕 민호! 함수가 이해하기 어려울 수 있지만 재미있는 예를 들어 설명해볼게.

함수는 특정 작업을 수행하는 코드 묶음이야. 마치 네가 가지고 있는 장난감 상자와 비슷해.

예를 들어, 마인크래프트에서 집을 지을 때 매번 같은 과정을 반복하지? 기초를 놓고, 벽을 세우고, 지붕을 올리고... 이런 과정을 하나의 함수로 만들 수 있어.

```python
def build_house(x, y, z, size):
    # x, y, z는 집을 지을 위치
    # size는 집의 크기
    place_foundation(x, y, z, size)
    build_walls(x, y, z, size)
    add_roof(x, y, z, size)
    add_door(x, y, z)
    print("집 완성!")

# 이제 함수를 호출해서 집을 지을 수 있어
build_house(10, 0, 15, "중간")
build_house(30, 0, 25, "큰")
```

이렇게 `build_house`라는 함수를 한 번 만들어두면, 다른 위치에 다른 크기의 집을
쉽게 지을 수 있어. 마치 레고 설명서처럼 한 번 만들어두고 계속 사용할 수 있지!

함수를 사용하면:
1. 같은 코드를 반복해서 작성하지 않아돼
2. 코드를 정리하기 쉬워져
3. 나중에 수정할 때도 한 곳만 바꾸면 돼

함수에 대해 더 궁금한 점이 있니?
        """
    }
}

# App configuration
st.set_page_config(
    page_title="CodeMate - 코딩 AI 튜터 데모",
    page_icon="🤖",
    layout="wide"
)

# 정적 파일 제공 설정
def get_logo_path():
    return LOGO_URL

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Login page
def show_login():
    # 전체 배경 컨테이너
    with st.container():
        st.markdown("""
        <style>
        .login-header {
            text-align: center;
            padding: 1rem 0;
            color: #4B7BEC;
        }
        .login-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            background-color: #ffffff;
        }
        .login-form {
            padding: 1.5rem;
        }
        .logo-container {
            text-align: center;
            padding: 1rem;
        }
        .centered-text {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # 로그인 헤더
        st.markdown('<h1 class="login-header">🤖 CodeMate - AI 코딩 튜터</h1>', unsafe_allow_html=True)
        
        # 두 개 컬럼으로 나누기
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            # 로고와 슬로건
            st.markdown('<h1 style="font-size: 80px; text-align: center;">👦</h1>', unsafe_allow_html=True)
            st.markdown('<h3 class="centered-text">개인 맞춤형 학습 경험</h3>', unsafe_allow_html=True)
            st.markdown('<p class="centered-text">학생의 관심사와 학습 스타일에 맞춘<br>지능형 코딩 교육</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
