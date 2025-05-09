import os
import streamlit as st
import json
import random
import time
from datetime import datetime
from io import StringIO
import sys

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
    },
    "variable": {
        "question": "변수가 뭐에요?",
        "answer": """
안녕 민호! 변수는 데이터를 저장하는 상자라고 생각하면 돼. 마인크래프트에서 인벤토리처럼!

예를 들어볼게:

```python
# 마인크래프트에서 블록 개수를 세는 변수
블록_개수 = 0

# 블록을 놓을 때마다 개수가 증가
블록_개수 = 블록_개수 + 1
print(f"지금까지 {블록_개수}개의 블록을 놓았어요!")

# 다이아몬드 개수를 저장하는 변수
다이아몬드 = 5
print(f"내 인벤토리에 다이아몬드가 {다이아몬드}개 있어요!")
```

변수를 사용하면:
1. 데이터를 저장할 수 있어 (블록 개수, 다이아몬드 개수 등)
2. 나중에 그 데이터를 다시 사용할 수 있어
3. 데이터가 바뀔 때마다 자동으로 업데이트돼

마치 마인크래프트에서 인벤토리에 아이템을 넣어두고 나중에 사용하는 것과 비슷하지!

변수에 대해 더 궁금한 점이 있니?
        """
    }
}

# Practice problems for code practice tab
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
        },
        "변수와 연산자": {
            "title": "마인크래프트 인벤토리 관리",
            "description": "마인크래프트 인벤토리의 아이템 개수를 관리하는 프로그램을 작성하세요.",
            "template": """def manage_inventory():
    # 여기에 코드를 작성하세요
    inventory = {
        "다이아몬드": 5,
        "철": 10,
        "나무": 20
    }
    
    # 인벤토리 출력
    print("현재 인벤토리:")
    for item, count in inventory.items():
        print(f"{item}: {count}개")
    
    # 아이템 추가
    item = input("어떤 아이템을 추가할까요? (다이아몬드, 철, 나무): ")
    amount = int(input("몇 개를 추가할까요? "))
    
    if item in inventory:
        inventory[item] += amount
        print(f"{item} {amount}개를 추가했습니다!")
    else:
        print("그런 아이템은 없습니다!")
    
    # 최종 인벤토리 출력
    print("\\n최종 인벤토리:")
    for item, count in inventory.items():
        print(f"{item}: {count}개")

# 함수 실행
manage_inventory()""",
            "hint": "딕셔너리의 값을 수정하는 방법을 사용해보세요!",
            "next_steps": "이제 이 인벤토리를 이용해서 자동으로 아이템을 사용하는 방법을 배워볼까요?"
        }
    },
    "중급": {
        "함수": {
            "title": "마인크래프트 자동 건축",
            "description": "마인크래프트에서 자동으로 건물을 짓는 함수를 만들어보세요.",
            "template": """def build_house(x, y, z, size):
    # 이 함수는 주어진 위치에 size 크기의 집을 지어야 합니다
    print(f"위치 ({x}, {y}, {z})에 {size} 크기의 집을 짓기 시작합니다!")
    
    # 기초 공사
    print("1. 기초 공사 중...")
    for i in range(size):
        print(f"   - 기초 블록 {i+1}/{size} 설치")
    
    # 벽 건설
    print("2. 벽 건설 중...")
    for i in range(size):
        print(f"   - 벽 블록 {i+1}/{size} 설치")
    
    # 지붕 설치
    print("3. 지붕 설치 중...")
    for i in range(size):
        print(f"   - 지붕 블록 {i+1}/{size} 설치")
    
    print(f"집이 완성되었습니다! 위치: ({x}, {y}, {z}), 크기: {size}")

# 함수 실행
build_house(10, 0, 15, 5)""",
            "hint": "집을 지을 때는 기초 → 벽 → 지붕 순서로 만들어보세요!",
            "next_steps": "다음으로는 더 복잡한 건물을 자동으로 짓는 방법을 배워볼까요?"
        }
    },
    "고급": {
        "클래스와 객체": {
            "title": "마인크래프트 모드 개발",
            "description": "마인크래프트 모드의 새로운 몬스터 클래스를 구현하세요.",
            "template": """class MinecraftMonster:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        print(f"{name}이(가) 생성되었습니다! 체력: {health}, 공격력: {attack_power}")
    
    def attack(self, target):
        print(f"{self.name}이(가) {target}을(를) 공격합니다!")
        print(f"공격력 {self.attack_power}의 데미지를 입혔습니다!")
    
    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name}이(가) {amount}의 데미지를 입었습니다!")
        print(f"남은 체력: {self.health}")
        if self.health <= 0:
            print(f"{self.name}이(가) 쓰러졌습니다!")

# 몬스터 생성 및 테스트
zombie = MinecraftMonster("좀비", 20, 5)
zombie.attack("플레이어")
zombie.take_damage(10)
zombie.take_damage(15)""",
            "hint": "몬스터의 상태를 클래스 변수로 관리하면 좋아요!",
            "next_steps": "이제 이 몬스터들을 서버에서 관리하는 방법을 배워볼까요?"
        },
        "예외 처리": {
            "title": "마인크래프트 서버 관리",
            "description": "마인크래프트 서버의 플레이어 데이터를 관리하는 프로그램을 작성하세요.",
            "template": """def manage_server_data():
    # 여기에 코드를 작성하세요
    players = {
        "player1": {"level": 10, "items": ["다이아몬드 검", "철 갑옷"]},
        "player2": {"level": 5, "items": ["나무 검", "가죽 갑옷"]}
    }
    
    try:
        # 플레이어 데이터 출력
        print("서버 플레이어 목록:")
        for player, data in players.items():
            print(f"\\n{player}:")
            print(f"  레벨: {data['level']}")
            print(f"  아이템: {', '.join(data['items'])}")
        
        # 플레이어 검색
        search_player = input("\\n검색할 플레이어 이름을 입력하세요: ")
        if search_player in players:
            print(f"\\n{search_player}의 정보:")
            print(f"레벨: {players[search_player]['level']}")
            print(f"아이템: {', '.join(players[search_player]['items'])}")
        else:
            print(f"\\n{search_player} 플레이어를 찾을 수 없습니다!")
            
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
        print("서버 데이터를 다시 확인해주세요.")

# 함수 실행
manage_server_data()""",
            "hint": "서버 데이터를 안전하게 저장하고 불러오는 방법을 생각해보세요!",
            "next_steps": "축하합니다! 이제 마인크래프트 모드 개발의 기초를 모두 배웠어요!"
        }
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
            # 로봇 이미지 추가
            st.markdown("""
            <div style='text-align: center;'>
                <img src='https://raw.githubusercontent.com/streamlit/streamlit/main/docs/images/logo.png' 
                     style='width: 200px; height: 200px; object-fit: contain;'>
            </div>
            """, unsafe_allow_html=True)
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
                
                # 추가 질문 버튼
                st.markdown("### 더 궁금한 점이 있으신가요?")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("예제 코드 보여줘"):
                        st.code("""
# 마인크래프트에서 블록 놓기 예제
def place_blocks():
    for i in range(5):
        print(f"{i+1}번째 블록을 놓았습니다!")
        time.sleep(1)  # 1초 대기
""", language="python")
                
                with col2:
                    if st.button("실습 문제 풀기"):
                        st.info("""
                        ### 실습 문제
                        1. 10개의 블록을 자동으로 놓는 코드를 작성해보세요.
                        2. 블록을 놓을 때마다 현재까지 놓은 블록의 개수를 출력하세요.
                        3. 마지막에 총 놓은 블록의 개수를 출력하세요.
                        """)
                
                with col3:
                    if st.button("다음 단계 학습하기"):
                        st.success("""
                        ### 다음 단계 학습 내용
                        1. 조건문을 사용한 블록 놓기
                        2. 함수를 사용한 자동 건축
                        3. 클래스를 사용한 마인크래프트 모드 만들기
                        """)
        
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
            st.subheader("📈 나의 마인크래프트 코딩 여정")
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
            
            # 문제 목록 (예시)
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
                    },
                    "변수와 연산자": {
                        "title": "마인크래프트 인벤토리 관리",
                        "description": "마인크래프트 인벤토리의 아이템 개수를 관리하는 프로그램을 작성하세요.",
                        "template": """def manage_inventory():
    # 여기에 코드를 작성하세요
    inventory = {
        "다이아몬드": 5,
        "철": 10,
        "나무": 20
    }
    
    # 인벤토리 출력
    print("현재 인벤토리:")
    for item, count in inventory.items():
        print(f"{item}: {count}개")
    
    # 아이템 추가
    item = input("어떤 아이템을 추가할까요? (다이아몬드, 철, 나무): ")
    amount = int(input("몇 개를 추가할까요? "))
    
    if item in inventory:
        inventory[item] += amount
        print(f"{item} {amount}개를 추가했습니다!")
    else:
        print("그런 아이템은 없습니다!")
    
    # 최종 인벤토리 출력
    print("\\n최종 인벤토리:")
    for item, count in inventory.items():
        print(f"{item}: {count}개")

# 함수 실행
manage_inventory()""",
                        "hint": "딕셔너리의 값을 수정하는 방법을 사용해보세요!",
                        "next_steps": "이제 이 인벤토리를 이용해서 자동으로 아이템을 사용하는 방법을 배워볼까요?"
                    }
                },
                "중급": {
                    "함수": {
                        "title": "마인크래프트 자동 건축",
                        "description": "마인크래프트에서 자동으로 건물을 짓는 함수를 만들어보세요.",
                        "template": """def build_house(x, y, z, size):
    # 이 함수는 주어진 위치에 size 크기의 집을 지어야 합니다
    print(f"위치 ({x}, {y}, {z})에 {size} 크기의 집을 짓기 시작합니다!")
    
    # 기초 공사
    print("1. 기초 공사 중...")
    for i in range(size):
        print(f"   - 기초 블록 {i+1}/{size} 설치")
    
    # 벽 건설
    print("2. 벽 건설 중...")
    for i in range(size):
        print(f"   - 벽 블록 {i+1}/{size} 설치")
    
    # 지붕 설치
    print("3. 지붕 설치 중...")
    for i in range(size):
        print(f"   - 지붕 블록 {i+1}/{size} 설치")
    
    print(f"집이 완성되었습니다! 위치: ({x}, {y}, {z}), 크기: {size}")

# 함수 실행
build_house(10, 0, 15, 5)""",
                        "hint": "집을 지을 때는 기초 → 벽 → 지붕 순서로 만들어보세요!",
                        "next_steps": "다음으로는 더 복잡한 건물을 자동으로 짓는 방법을 배워볼까요?"
                    },
                    "리스트와 딕셔너리": {
                        "title": "마인크래프트 모드 아이템 관리",
                        "description": "마인크래프트 모드의 새로운 아이템을 관리하는 프로그램을 작성하세요.",
                        "template": """def manage_mod_items():
    # 여기에 코드를 작성하세요
    mod_items = {
        "마법 지팡이": {"공격력": 10, "내구도": 100},
        "텔레포트 링": {"사용 횟수": 3, "쿨다운": 60}
    }
    
    # 아이템 목록 출력
    print("사용 가능한 아이템:")
    for item, stats in mod_items.items():
        print(f"\\n{item}:")
        for stat, value in stats.items():
            print(f"  - {stat}: {value}")
    
    # 아이템 사용
    item = input("\\n어떤 아이템을 사용할까요? (마법 지팡이, 텔레포트 링): ")
    
    if item in mod_items:
        print(f"\\n{item} 사용 중...")
        if item == "마법 지팡이":
            mod_items[item]["내구도"] -= 10
            print(f"마법 지팡이의 남은 내구도: {mod_items[item]['내구도']}")
        elif item == "텔레포트 링":
            mod_items[item]["사용 횟수"] -= 1
            print(f"텔레포트 링의 남은 사용 횟수: {mod_items[item]['사용 횟수']}")
    else:
        print("그런 아이템은 없습니다!")

# 함수 실행
manage_mod_items()""",
                        "hint": "아이템의 속성을 딕셔너리로 관리하면 편리해요!",
                        "next_steps": "이제 이 아이템들을 사용하는 새로운 몬스터를 만들어볼까요?"
                    }
                },
                "고급": {
                    "클래스와 객체": {
                        "title": "마인크래프트 모드 개발",
                        "description": "마인크래프트 모드의 새로운 몬스터 클래스를 구현하세요.",
                        "template": """class MinecraftMonster:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        print(f"{name}이(가) 생성되었습니다! 체력: {health}, 공격력: {attack_power}")
    
    def attack(self, target):
        print(f"{self.name}이(가) {target}을(를) 공격합니다!")
        print(f"공격력 {self.attack_power}의 데미지를 입혔습니다!")
    
    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name}이(가) {amount}의 데미지를 입었습니다!")
        print(f"남은 체력: {self.health}")
        if self.health <= 0:
            print(f"{self.name}이(가) 쓰러졌습니다!")

# 몬스터 생성 및 테스트
zombie = MinecraftMonster("좀비", 20, 5)
zombie.attack("플레이어")
zombie.take_damage(10)
zombie.take_damage(15)""",
                        "hint": "몬스터의 상태를 클래스 변수로 관리하면 좋아요!",
                        "next_steps": "이제 이 몬스터들을 서버에서 관리하는 방법을 배워볼까요?"
                    },
                    "예외 처리": {
                        "title": "마인크래프트 서버 관리",
                        "description": "마인크래프트 서버의 플레이어 데이터를 관리하는 프로그램을 작성하세요.",
                        "template": """def manage_server_data():
    # 여기에 코드를 작성하세요
    players = {
        "player1": {"level": 10, "items": ["다이아몬드 검", "철 갑옷"]},
        "player2": {"level": 5, "items": ["나무 검", "가죽 갑옷"]}
    }
    
    try:
        # 플레이어 데이터 출력
        print("서버 플레이어 목록:")
        for player, data in players.items():
            print(f"\\n{player}:")
            print(f"  레벨: {data['level']}")
            print(f"  아이템: {', '.join(data['items'])}")
        
        # 플레이어 검색
        search_player = input("\\n검색할 플레이어 이름을 입력하세요: ")
        if search_player in players:
            print(f"\\n{search_player}의 정보:")
            print(f"레벨: {players[search_player]['level']}")
            print(f"아이템: {', '.join(players[search_player]['items'])}")
        else:
            print(f"\\n{search_player} 플레이어를 찾을 수 없습니다!")
            
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
        print("서버 데이터를 다시 확인해주세요.")

# 함수 실행
manage_server_data()""",
                        "hint": "서버 데이터를 안전하게 저장하고 불러오는 방법을 생각해보세요!",
                        "next_steps": "축하합니다! 이제 마인크래프트 모드 개발의 기초를 모두 배웠어요!"
                    }
                }
            }
            
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
                    # 사용자 입력 처리
                    user_input = user_code
                    if not user_input:
                        st.warning("코드를 입력해주세요!")
                        return

                    # 입력값 처리
                    input_values = {}
                    for i, input_field in enumerate(input_fields):
                        key = f"input_{i}"
                        if key in st.session_state:
                            input_values[i] = st.session_state[key]

                    # 코드 실행 결과 표시
                    with st.expander("실행 결과", expanded=True):
                        # 표준 출력과 에러를 캡처하기 위한 StringIO 객체
                        output = StringIO()
                        error_output = StringIO()
                        sys.stdout = output
                        sys.stderr = error_output

                        # 입력값을 처리하기 위한 mock_input 함수
                        def mock_input(prompt):
                            # prompt에서 입력 번호 추출
                            try:
                                input_num = int(prompt.split()[1]) - 1
                                return input_values.get(input_num, "0")  # 기본값 0으로 설정
                            except:
                                return "0"  # 기본값 0으로 설정

                        # 코드 실행
                        try:
                            # 코드 실행 전에 필요한 변수 초기화
                            block_type = "돌"  # 기본값 설정
                            count = 1  # 기본값 설정

                            # 코드 실행
                            exec(user_input, {"input": mock_input, "print": print, "range": range, "len": len, "str": str, "int": int, "float": float, "list": list, "dict": dict, "set": set, "tuple": tuple, "True": True, "False": False, "None": None, "block_type": block_type, "count": count})

                            # 실행 결과 가져오기
                            result = output.getvalue()
                            error = error_output.getvalue()

                            # 결과 표시
                            if result:
                                # 결과를 더 보기 좋게 포맷팅
                                formatted_result = result.replace("번째", "번째 🧱").replace("블록을 놓았습니다", "블록을 놓았습니다! 🎮").replace("총", "총 🎯").replace("개의", "개의 🧱").replace("블록을 놓았습니다", "블록을 놓았습니다! 🎮")
                                st.success("코드가 성공적으로 실행되었습니다! 🎉")
                                st.code(formatted_result, language="python")
                                
                                # 성공 시나리오 피드백
                                st.info("""
                                🎮 마인크래프트 관련 기능이 잘 구현되었습니다!
                                다음 단계를 제안합니다:
                                1. 코드를 더 효율적으로 개선해보세요
                                2. 다른 입력값으로 테스트해보세요
                                3. 새로운 기능을 추가해보세요
                                """)
                            if error:
                                st.error("실행 중 오류가 발생했습니다:")
                                st.code(error, language="python")
                                
                                # 오류 발생 시나리오 피드백
                                if "NameError" in error:
                                    st.warning("""
                                    🔍 변수나 함수 이름이 정의되지 않았습니다.
                                    해결 방법: 변수나 함수를 사용하기 전에 정의했는지 확인하세요.
                                    예시: `block_type = "돌"`과 같이 변수를 먼저 정의해야 합니다.
                                    """)
                                elif "SyntaxError" in error:
                                    st.warning("""
                                    🔍 코드 문법에 오류가 있습니다.
                                    해결 방법: 괄호, 들여쓰기, 콜론 등을 확인하세요.
                                    예시: `if` 문 뒤에는 콜론(`:`)이 필요합니다.
                                    """)
                                elif "TypeError" in error:
                                    st.warning("""
                                    🔍 데이터 타입이 맞지 않습니다.
                                    해결 방법: 문자열과 숫자를 함께 사용할 때는 형변환이 필요합니다.
                                    예시: `str(count)`로 숫자를 문자열로 변환하세요.
                                    """)
                                else:
                                    st.warning("""
                                    🔍 다른 오류가 발생했습니다.
                                    해결 방법: 코드를 다시 한 번 확인해보세요.
                                    힌트: 문제의 힌트를 참고하거나 선생님과 상담해보세요.
                                    """)

                        except Exception as e:
                            st.error(f"실행 중 오류가 발생했습니다: {str(e)}")
                            st.warning("""
                            🔍 오류가 발생했습니다.
                            해결 방법: 코드를 다시 한 번 확인해보세요.
                            힌트: 문제의 힌트를 참고하거나 선생님과 상담해보세요.
                            """)
                        finally:
                            # 표준 출력과 에러를 원래대로 복구
                            sys.stdout = sys.__stdout__
                            sys.stderr = sys.__stderr__
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
