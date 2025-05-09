import os
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
        st.title("🤖 CodeMate")
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
    st.title("CodeMate와 함께 코딩을 배워보세요! 👨‍💻")
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
                elif "변수" in custom_question:
                    st.session_state.current_question = "variable"
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
                            <span style='font-size: 24px; margin-right: 10px;'>👨‍💻</span>
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
            
            # 개인화된 추천 섹션 추가
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
            
            # 추천 문제 섹션
            st.subheader("🎯 추천 문제")
            st.info("""
            마인크래프트를 좋아하시는 {}님을 위한 맞춤형 문제를 준비했어요!
            지금까지 함수와 반복문을 배웠으니, 이번에는 마인크래프트에서 자동으로 건물을 짓는 프로그램을 만들어볼까요?
            """.format(SAMPLE_USER['name']))
            
            # 난이도 선택
            difficulty = st.selectbox(
                "난이도 선택",
                ["초급", "중급", "고급"]
            )
            
            # 주제 선택
            topic = st.selectbox(
                "주제 선택",
                ["마인크래프트 기초", "변수와 연산자", "조건문", "반복문", "함수", "리스트와 딕셔너리", "클래스와 객체", "파일 입출력", "예외 처리"]
            )
            
            # 문제 유형 선택
            problem_type = st.selectbox(
                "문제 유형",
                ["코드 완성하기", "버그 수정하기", "알고리즘 구현하기", "코드 최적화하기", "코드 리팩토링하기"]
            )
            
            # 학습 경로 표시
            st.subheader("�� 나의 마인크래프트 코딩 여정")
            learning_path = [
                {"step": 1, "title": "기본 블록 놓기", "status": "완료", "icon": "✅"},
                {"step": 2, "title": "자동 건축 기초", "status": "완료", "icon": "✅"},
                {"step": 3, "title": "인벤토리 관리", "status": "진행 중", "icon": "🔄"},
                {"step": 4, "title": "모드 개발 기초", "status": "예정", "icon": "⏳"},
                {"step": 5, "title": "서버 관리", "status": "예정", "icon": "⏳"}
            ]
            
            for step in learning_path:
                st.markdown(f"""
                {step['icon']} **Step {step['step']}**: {step['title']} - {step['status']}
                """)
            
            # 선택된 문제 표시
            if difficulty in practice_problems and topic in practice_problems[difficulty]:
                problem = practice_problems[difficulty][topic]
                st.subheader(f"📝 {problem['title']}")
                st.info(problem['description'])
                
                # 힌트 표시 (접을 수 있는 섹션)
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
                        # 표준 입출력 리다이렉션을 위한 설정
                        import sys
                        from io import StringIO
                        import contextlib

                        # 사용자 입력을 처리하기 위한 입력 버퍼
                        input_buffer = []
                        def mock_input(prompt=""):
                            if not input_buffer:
                                # 사용자로부터 입력 받기
                                user_input = st.text_input(prompt, key=f"input_{len(input_buffer)}")
                                if user_input:
                                    input_buffer.append(user_input)
                                    return user_input
                                return ""
                            return input_buffer.pop(0)

                        # 표준 출력을 캡처하기 위한 StringIO 객체
                        output = StringIO()
                        
                        # 코드 실행
                        with contextlib.redirect_stdout(output):
                            # input 함수를 mock_input으로 대체
                            sys.modules['builtins'].input = mock_input
                            exec(user_code)
                            # 원래 input 함수로 복원
                            sys.modules['builtins'].input = input

                        # 실행 결과 표시
                        result = output.getvalue()
                        if result:
                            # 결과를 더 보기 좋게 포맷팅
                            formatted_result = ""
                            for line in result.split('\n'):
                                if line.strip():
                                    if "블록을 놓았습니다" in line:
                                        formatted_result += f"🎮 {line}\n"
                                    elif "집을 짓기 시작합니다" in line:
                                        formatted_result += f"🏠 {line}\n"
                                    elif "기초 공사" in line or "벽 건설" in line or "지붕 설치" in line:
                                        formatted_result += f"🏗️ {line}\n"
                                    elif "생성되었습니다" in line:
                                        formatted_result += f"👾 {line}\n"
                                    elif "공격합니다" in line:
                                        formatted_result += f"⚔️ {line}\n"
                                    elif "데미지를 입혔습니다" in line or "데미지를 입었습니다" in line:
                                        formatted_result += f"💥 {line}\n"
                                    elif "쓰러졌습니다" in line:
                                        formatted_result += f"💀 {line}\n"
                                    else:
                                        formatted_result += f"{line}\n"
                            
                            st.markdown(f"""
                            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                <pre style='margin: 0;'>{formatted_result}</pre>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.success("코드가 성공적으로 실행되었습니다!")
                        
                        # 피드백 제공
                        st.info("""
                        ### 피드백
                        - 코드가 정상적으로 실행되었습니다.
                        - 마인크래프트 관련 기능이 잘 구현되었습니다.
                        - 다음 단계로 넘어갈 준비가 되었습니다!
                        """)
                        
                        # 다음 단계 제안
                        st.markdown(f"""
                        ### 다음 단계
                        {problem['next_steps']}
                        - 코드를 더 효율적으로 개선해보세요.
                        - 다른 입력값으로 테스트해보세요.
                        - 예외 처리를 추가해보세요.
                        """)
                        
                    except Exception as e:
                        st.error(f"코드 실행 중 오류가 발생했습니다: {str(e)}")
                        st.info("""
                        ### 도움이 필요하신가요?
                        - 힌트를 확인해보세요.
                        - 선생님과 연결하기를 통해 도움을 받을 수 있습니다.
                        - 다른 난이도의 문제를 시도해보세요.
                        """)
            else:
                st.info("선택한 난이도와 주제에 맞는 문제가 준비 중입니다.")
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
            import plotly.express as px
            
            # Convert timeline data to DataFrame format
            import pandas as pd
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
st.caption("© 2025 CodeMate - 개인화된 AI 코딩 튜터")
