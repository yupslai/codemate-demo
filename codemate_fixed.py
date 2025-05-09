import os
import streamlit as st
import json
import random
import time
from datetime import datetime

# 로고 URL 설정
LOGO_URL = "https://raw.githubusercontent.com/openai/openai-python/main/assets/logo.png"

# Simulated user data
SAMPLE_USER = {
    "id": "user123",
    "name": "Minho",
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
"""
    },
    "debugging": {
        "question": "이 코드가 왜 안 되는지 모르겠어요: for i in range(10) print(i)",
        "answer": "..."
    },
    "function": {
        "question": "함수가 뭐에요?",
        "answer": "..."
    }
}

# App configuration
st.set_page_config(
    page_title="CodeMate - 코딩 AI 튜터 데모",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    # Login page
def show_login():
    with st.container():
        st.markdown("""
        <style>
        .login-header {
            text-align: center;
            padding: 1rem 0;
            color: #4B7BEC;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-header">👦 CodeMate - AI 코딩 튜터</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<h3 class="centered-text">개인 맞춤형 학습 경험</h3>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("계정 로그인")
            user_id = st.text_input("사용자 ID:", value="user123")
            password = st.text_input("비밀번호:", value="demo1234", type="password")
            
            if st.button("로그인"):
                with st.spinner("로그인 중..."):
                    time.sleep(1)
                    st.session_state.logged_in = True
                    st.experimental_rerun()

def show_main_app():
    # Sidebar
    with st.sidebar:
        st.title("👦 CodeMate")
        st.write(f"**안녕, {SAMPLE_USER['name']}!**")
        st.write(f"**나이:** {SAMPLE_USER['age']}세")
        st.write(f"**학년:** {SAMPLE_USER['grade']}학년")
        st.write("**관심사:**")
        for interest in SAMPLE_USER['interests']:
            st.write(f"- {interest}")
        
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.experimental_rerun()
    
    # Main content
    st.title("CodeMate와 함께 코딩을 배워보세요! 👨‍💻")
    tabs = st.tabs(["질문하기", "코드 연습", "학습 분석", "선생님 연결하기"])
    # Tab 2: Code practice
with tabs[1]:
    st.header("코드 연습")
    
    # 개인화된 추천 섹션
    st.markdown("""
    ### 🎮 마인크래프트 코딩 여정
    안녕하세요, {}님! 마인크래프트를 좋아하시는 당신을 위한 특별한 코딩 연습을 준비했어요.
    """.format(SAMPLE_USER['name']))
    
    # 학습 진행도 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("완료한 마인크래프트 문제", "3개")
    with col2:
        st.metric("다음 목표까지", "2문제")
    with col3:
        st.metric("획득한 마인크래프트 배지", "🏆 2개")
    
    # 난이도 선택
    difficulty = st.selectbox(
        "난이도 선택",
        ["초급", "중급", "고급"]
    )
    
    # 주제 선택
    topic = st.selectbox(
        "주제 선택",
        ["마인크래프트 기초", "변수와 연산자", "조건문", "반복문", "함수"]
    )
    
    # 문제 목록
    practice_problems = {
        "초급": {
            "마인크래프트 기초": {
                "title": "마인크래프트 블록 놓기",
                "description": "마인크래프트에서 블록을 놓는 간단한 프로그램을 작성하세요.",
                "template": """def place_block():
    # 여기에 코드를 작성하세요
    block_type = input("어떤 블록을 놓을까요? (돌, 나무, 흙): ")
    count = int(input("몇 개를 놓을까요? "))
    
    # 블록을 놓는 코드를 작성하세요
    for i in range(count):
        print(f"{i+1}번째 {block_type} 블록을 놓았습니다!")
    print(f"총 {count}개의 {block_type} 블록을 놓았습니다!")

# 함수 실행
place_block()""",
                "hint": "for 반복문을 사용해서 블록을 여러 개 놓아보세요!",
                "next_steps": "다음으로는 자동으로 건물을 짓는 방법을 배워볼까요?"
            }
        }
    }
    
    # 선택된 문제 표시
    if difficulty in practice_problems and topic in practice_problems[difficulty]:
        problem = practice_problems[difficulty][topic]
        st.subheader(f"📝 {problem['title']}")
        st.info(problem['description'])
        
        with st.expander("💡 힌트 보기"):
            st.write(problem['hint'])
        
        # 코드 작성 영역
        user_code = st.text_area(
            "코드를 여기에 작성하세요:",
            value=problem['template'],
            height=250
        )
        
        # 실행 버튼
        if st.button("실행하기"):
            st.subheader("실행 결과:")
            try:
                # 표준 입출력 리다이렉션
                import sys
                from io import StringIO
                import contextlib

                # 사용자 입력 처리
                input_buffer = []
                def mock_input(prompt=""):
                    if not input_buffer:
                        user_input = st.text_input(prompt, key=f"input_{len(input_buffer)}")
                        if user_input:
                            input_buffer.append(user_input)
                            return user_input
                        return ""
                    return input_buffer.pop(0)

                # 코드 실행
                output = StringIO()
                with contextlib.redirect_stdout(output):
                    sys.modules['builtins'].input = mock_input
                    exec(user_code)
                    sys.modules['builtins'].input = input

                # 결과 표시
                result = output.getvalue()
                if result:
                    st.code(result, language="plaintext")
                
                st.success("코드가 성공적으로 실행되었습니다!")
                
                # 피드백 및 다음 단계
                st.info("### 피드백\n- 코드 구조가 잘 작성되었습니다.\n- 변수명이 명확합니다.")
                st.markdown(f"### 다음 단계\n{problem['next_steps']}")
                
            except Exception as e:
                st.error(f"코드 실행 중 오류가 발생했습니다: {str(e)}")

# Main logic
if st.session_state.logged_in:
    show_main_app()
else:
    show_login()

# Footer
st.divider()
st.caption("© 2025 CodeMate - 개인화된 AI 코딩 튜터")
