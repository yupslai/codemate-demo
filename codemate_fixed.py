import os
import streamlit as st
import json
import random
import time
from datetime import datetime
import pandas as pd
import plotly.express as px

# 로고 URL 설정 (로컬 파일 대신 URL 사용)
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
        st.markdown('<h1 class="login-header">�� CodeMate - AI 코딩 튜터</h1>', unsafe_allow_html=True)
        
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
            st.markdown('<div class="login-form">', unsafe_allow_html=True)
            st.subheader("계정 로그인")
            
            # 아이디 입력
            user_id = st.text_input("사용자 ID:", value="user123", 
                                   placeholder="사용자 ID를 입력하세요")
            
            # 비밀번호 입력
            password = st.text_input("비밀번호:", value="demo1234", 
                                    type="password", 
                                    placeholder="비밀번호를 입력하세요")
            
            # 로그인 버튼
            if st.button("로그인", key="login_button", 
                         help="데모 계정: user123 / demo1234"):
                with st.spinner("로그인 중..."):
                    time.sleep(1)  # Simulate API call
                    st.session_state.logged_in = True
                    st.experimental_rerun()
                    
            st.markdown('<div style="text-align: center; margin-top: 20px;">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main application
def show_main_app():
    # Sidebar
    with st.sidebar:
        st.title("�� 코드메이트")
        st.write(f"**안녕, {SAMPLE_USER['name']}!**")
        st.write(f"**나이:** {SAMPLE_USER['age']}세")
        st.write(f"**학년:** {SAMPLE_USER['grade']}학년")
        st.write("**관심사:**")
        for interest in SAMPLE_USER['interests']:
            st.write(f"- {interest}")
        
        st.divider()
        
        # Learning progress summary
        st.subheader("학습 현황")
        mastered = sum(1 for c in LEARNING_HISTORY['concepts'] if c['understanding_level'] >= 4)
        learning = sum(1 for c in LEARNING_HISTORY['concepts'] if 2 <= c['understanding_level'] < 4)
        struggling = sum(1 for c in LEARNING_HISTORY['concepts'] if c['understanding_level'] < 2)
        
        st.write(f"**마스터:** {mastered}/{len(LEARNING_HISTORY['concepts'])}")
        st.write(f"**학습 중:** {learning}/{len(LEARNING_HISTORY['concepts'])}")
        st.write(f"**어려움:** {struggling}/{len(LEARNING_HISTORY['concepts'])}")
        
        # Concept strength visualization
        st.subheader("개념 이해도")
        for concept in LEARNING_HISTORY['concepts']:
            level_text = f"{concept['name']}: "
            level = concept['understanding_level']
            filled = "🟩" * level
            empty = "⬜" * (5 - level)
            st.write(level_text + filled + empty)
        
        st.divider()
        
        # 선생님 연결하기 버튼
        if st.button("👨‍🏫 선생님과 연결하기", help="코딩 문제로 어려움을 겪고 계신가요? 선생님과 연결해보세요!"):
            st.session_state.show_teacher_connection = True
            st.experimental_rerun()
        
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.experimental_rerun()
    
    # Main content
    st.title("코드메이트와 함께 코딩을 배워보세요! ��‍💻")
    
    # 선생님 연결하기 버튼이 클릭되었는지 확인
    if st.session_state.get('show_teacher_connection', False):
        show_teacher_connection()
        # 상태 초기화
        st.session_state.show_teacher_connection = False
    else:
        tabs = st.tabs(["질문하기", "코드 연습", "학습 분석", "선생님 연결하기"])
        
        # Tab 1: Ask questions
        with tabs[0]:
            st.header("무엇이든 물어보세요!")
            
            # Demo questions
            st.subheader("질문 예시")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("while 반복문이 뭐야?"):
                    st.session_state.current_question = "while_loop"
            
            with col2:
                if st.button("이 코드 오류 찾아줘"):
                    st.session_state.current_question = "debugging"
            
            with col3:
                if st.button("함수가 뭐에요?"):
                    st.session_state.current_question = "function"
            
            # Custom question
            custom_question = st.text_area("또는 직접 질문하기:", placeholder="여기에 질문을 입력하세요...")
            if st.button("질문하기") and custom_question:
                # For demo, redirect to one of our sample questions based on keywords
                if "while" in custom_question or "반복" in custom_question:
                    st.session_state.current_question = "while_loop"
                elif "오류" in custom_question or "에러" in custom_question or "디버깅" in custom_question:
                    st.session_state.current_question = "debugging"
                elif "함수" in custom_question:
                    st.session_state.current_question = "function"
                else:
                    # Default to function explanation for any other question
                    st.session_state.current_question = "function"
            
            # Display answer
            if st.session_state.current_question:
                question_key = st.session_state.current_question
                question = SAMPLE_QA[question_key]["question"]
                answer = SAMPLE_QA[question_key]["answer"]
                
                st.divider()
                
                # Add to chat history if not already there
                if not st.session_state.chat_history or st.session_state.chat_history[-1]['question'] != question:
                    st.session_state.chat_history.append({
                        'question': question, 
                        'answer': answer,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                
                # Display chat history
                for i, chat in enumerate(st.session_state.chat_history):
                    # Question
                    st.markdown(f"""
                    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin: 10px 0;'>
                        <div style='display: flex; align-items: center;'>
                            <span style='font-size: 24px; margin-right: 10px;'>👦</span>
                            <div>{chat['question']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Answer
                    st.markdown(f"""
                    <div style='background-color: #e6f3ff; padding: 10px; border-radius: 10px; margin: 10px 0;'>
                        <div style='display: flex; align-items: center;'>
                            <span style='font-size: 24px; margin-right: 10px;'>🤖</span>
                            <div>{chat['answer']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Tab 2: Code practice
        with tabs[1]:
            st.header("코드 연습")
            
            # Sample practice problem based on user's weak concept (functions)
            st.subheader("추천 연습 문제")
            st.info("함수에 대한 이해도를 높이기 위한 연습 문제입니다.")
            
            st.markdown("""
            ### 마인크래프트 블록 놓기 함수 만들기
            
            마인크래프트에서 여러 종류의 블록을 놓는 함수를 만들어보세요:
            
            ```python
            def place_blocks(block_type, count):
                # 이 함수는 주어진 유형의 블록을 count만큼 놓아야 합니다
                # 아래 코드를 완성하세요
                pass
            ```
            
            1. 함수가 블록 타입과 개수를 받도록 하세요
            2. 블록을 놓을 때마다 메시지를 출력하세요
            3. 모든 블록을 놓은 후 완료 메시지를 출력하세요
            """)
            
            user_code = st.text_area("코드를 여기에 작성하세요:", height=250, value="""def place_blocks(block_type, count):
    # 여기에 코드를 작성하세요
    for i in range(count):
        print(f"{block_type} 블록을 놓았습니다.")
        
    print(f"총 {count}개의 {block_type} 블록을 놓았습니다. 완료!")
    
# 함수 테스트
place_blocks("돌", 5)
""")
            
            if st.button("실행하기"):
                st.subheader("실행 결과:")
                
                # Simulate code execution
                output = st.code("""돌 블록을 놓았습니다.
돌 블록을 놓았습니다.
돌 블록을 놓았습니다.
돌 블록을 놓았습니다.
돌 블록을 놓았습니다.
총 5개의 돌 블록을 놓았습니다. 완료!""", language="plaintext")
                
                # Show feedback
                st.success("잘했어요! 함수를 올바르게 만들었습니다. 이제 다른 블록 타입과 개수로도 시도해보세요.")
                
                # Update learning progress
                for concept in LEARNING_HISTORY['concepts']:
                    if concept['id'] == 'fun001':  # Function concept ID
                        concept['understanding_level'] = min(5, concept['understanding_level'] + 1)
                        concept['last_practiced'] = datetime.now().strftime("%Y-%m-%d")
        
        # Tab 3: Learning analysis
        with tabs[2]:
            st.header("학습 분석")
            
            # Learning timeline with more detailed data
            st.subheader("📊 학습 타임라인")
            timeline_data = [
                {"date": "2025-05-15", "concept": "변수", "activity": "퀴즈 완료", "score": "90%", "time_spent": "45분"},
                {"date": "2025-05-18", "concept": "조건문", "activity": "실습 완료", "score": "75%", "time_spent": "60분"},
                {"date": "2025-05-20", "concept": "반복문", "activity": "과제 제출", "score": "60%", "time_spent": "90분"},
                {"date": "2025-05-22", "concept": "함수", "activity": "튜토리얼 완료", "score": "40%", "time_spent": "30분"}
            ]
            
            # Timeline visualization
            st.markdown("### 📈 학습 진행도 그래프")
            
            # Convert timeline data to DataFrame format
            df = pd.DataFrame(timeline_data)
            df['score'] = df['score'].str.rstrip('%').astype('float')
            
            # Create line chart
            fig = px.line(df, x='date', y='score', 
                          title='개념별 이해도 변화',
                          markers=True,
                          labels={'score': '이해도 (%)', 'date': '날짜'})
            fig.update_traces(line_color='#4B7BEC')
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed timeline table
            st.markdown("### 📅 상세 학습 이력")
            st.table(timeline_data)
            
            # Learning recommendations with more detail
            st.subheader("🎯 맞춤형 학습 경로")
            st.info("현재 학습 데이터를 기반으로 한 맞춤형 추천입니다.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 단기 목표 (2주)
                1. **함수** 이해도 향상 (현재 1/5)
                    - 함수 기초 연습 문제 5개 풀기
                    - 함수를 사용한 간단한 게임 만들기
                    - 예상 소요 시간: 4시간
                
                2. **반복문** 이해도 향상 (현재 2/5)
                    - while과 for 반복문 차이점 학습
                    - 중첩 반복문 연습하기
                    - 예상 소요 시간: 3시간
                """)
            
            with col2:
                st.markdown("""
                ### 장기 목표 (2개월)
                1. **마인크래프트 모드 만들기**
                    - 필요 개념: 변수, 조건문, 반복문, 함수
                    - 예상 완료 시간: 3주
                    - 난이도: ⭐⭐⭐
                
                2. **간단한 웹 게임 개발**
                    - HTML, CSS, JavaScript 기초 학습
                    - 예상 완료 시간: 2개월
                    - 난이도: ⭐⭐⭐⭐
                """)
            
            # Enhanced achievements system
            st.subheader("🏆 업적 시스템")
            
            # Achievement categories
            achievement_categories = {
                "기초 마스터": [
                    {"name": "첫 코드 작성", "icon": "🏆", "date": "2025-05-10", "progress": "100%"},
                    {"name": "변수 마스터", "icon": "🌟", "date": "2025-05-15", "progress": "100%"},
                    {"name": "반복문 탐험가", "icon": "🔄", "date": "2025-05-20", "progress": "60%"},
                    {"name": "조건부 논리", "icon": "❓", "date": "2025-05-18", "progress": "75%"}
                ],
                "프로젝트": [
                    {"name": "미니 게임 제작", "icon": "🎮", "date": "진행 중", "progress": "30%"},
                    {"name": "웹사이트 제작", "icon": "🌐", "date": "예정", "progress": "0%"}
                ],
                "특별 도전": [
                    {"name": "100일 코딩", "icon": "🔥", "date": "진행 중", "progress": "45%"},
                    {"name": "코드 리뷰어", "icon": "👀", "date": "예정", "progress": "0%"}
                ]
            }
            
            # Display achievements in tabs
            achievement_tabs = st.tabs(list(achievement_categories.keys()))
            
            for i, (category, achievements) in enumerate(achievement_categories.items()):
                with achievement_tabs[i]:
                    for achievement in achievements:
                        col1, col2, col3 = st.columns([1, 3, 1])
                        with col1:
                            st.markdown(f"### {achievement['icon']}")
                        with col2:
                            st.markdown(f"**{achievement['name']}**")
                            st.progress(float(achievement['progress'].rstrip('%')) / 100)
                        with col3:
                            st.caption(achievement['date'])
            
            # Learning statistics
            st.subheader("📊 학습 통계")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("총 학습 시간", "225분")
            with col2:
                st.metric("완료한 문제", "12개")
            with col3:
                st.metric("평균 점수", "66%")
            with col4:
                st.metric("획득한 업적", "4개")
        
        # Tab 4: Teacher connection
        with tabs[3]:
            show_teacher_connection()

def show_teacher_connection():
    st.title("👨‍🏫 선생님과 연결하기")
    
    # 뒤로가기 버튼 추가
    if st.button("← 메인 화면으로 돌아가기"):
        st.session_state.show_teacher_connection = False
        st.experimental_rerun()
    
    st.markdown("""
    ### 안녕하세요! 👋
    코딩 문제를 해결하는 데 어려움을 겪고 계신가요? 선생님과 연결하여 도움을 받아보세요.
    """)
    
    # 문제 설명 입력
    problem_description = st.text_area(
        "어떤 문제를 겪고 계신가요?",
        placeholder="문제 상황을 자세히 설명해주세요. 예: 코드가 실행되지 않아요, 특정 기능을 구현하는 방법을 모르겠어요 등",
        height=150
    )
    
    # 코드 공유 (선택사항)
    code_snippet = st.text_area(
        "관련 코드가 있다면 공유해주세요 (선택사항)",
        placeholder="문제가 발생하는 코드를 여기에 붙여넣어주세요",
        height=150
    )
    
    # 선생님 선택
    teacher_type = st.selectbox(
        "어떤 선생님의 도움이 필요하신가요?",
        ["Python 선생님", "웹 개발 선생님", "게임 개발 선생님", "기타"]
    )
    
    # 연락처 정보
    contact_info = st.text_input(
        "연락처 정보",
        placeholder="이메일 또는 전화번호를 입력해주세요"
    )
    
    # 제출 버튼
    if st.button("선생님 연결 요청하기"):
        if problem_description:
            st.success("요청이 성공적으로 접수되었습니다! 선생님이 곧 연락드릴 예정입니다.")
            st.info("평균 응답 시간: 24시간 이내")
        else:
            st.error("문제 설명을 입력해주세요.")
    
    # FAQ 섹션
    st.markdown("""
    ### 자주 묻는 질문
    
    **Q: 선생님은 어떤 분들인가요?**  
    A: 하버드, 콜롬비아, UC버클리, 스탠포드 Computer Science 전공자들입니다.
    
    **Q: 선생님 연결은 유료인가요?**  
    A: 네, 선생님 연결 서비스는 유료입니다. 구체적인 가격은 선생님과 상담 후 결정됩니다.
    
    **Q: 얼마나 빨리 응답을 받을 수 있나요?**  
    A: 일반적으로 24시간 이내에 응답을 받으실 수 있습니다.
    
    **Q: 어떤 종류의 문제를 도와드릴 수 있나요?**  
    A: 코딩 관련 모든 문제를 도와드립니다. 문법, 디버깅, 알고리즘, 아키텍처 등 다양한 영역의 선생님이 있습니다.
    """)

# Main logic
if st.session_state.logged_in:
    show_main_app()
else:
    show_login()

# Footer
st.divider()
st.caption("© 2025 코드메이트 - 개인화된 AI 코딩 튜터")
