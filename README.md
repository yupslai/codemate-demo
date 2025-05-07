# codemate-demo
CodeMate AI 코딩 튜터 데모
https://codemate-demo-knym2mlbegkgavichyfcxf.streamlit.app/

# CodeMate 데모 시나리오

## 개요
CodeMate는 7-16세 학생을 대상으로 하는 AI 코딩 튜터 시스템으로, RAG (Retrieval-Augmented Generation)와 MCP (Memory, Context, Persona) 기술을 활용한 개인화된 코딩 학습 경험을 제공합니다.

이 데모는 실제 제품의 주요 기능과 사용자 경험을 시연하기 위한 것입니다.

## 데모 실행 방법

### 필요 조건
- Python 3.8 이상
- Streamlit

### 설치 방법
```bash
# 필요한 패키지 설치
pip install streamlit

# 데모 실행
streamlit run codemate_demo_scenario.py
```

## 데모 시나리오

### 시나리오 1: 코딩 초보자 학습 경험
1. 로그인: 기본 사용자 계정(ID: user123, 비밀번호: demo1234)으로 로그인
2. 질문하기 탭에서 "while 반복문이 뭐야?" 질문을 선택
3. AI 튜터의 개인화된 응답 확인 (마인크래프트 관심사 기반)
4. "함수가 뭐에요?" 질문을 선택하여 새로운 개념 학습

### 시나리오 2: 코드 디버깅 지원
1. 질문하기 탭에서 "이 코드 오류 찾아줘" 버튼 선택
2. 오류 해석 및 수정 방법 확인
3. 코드 연습 탭으로 이동하여 실습 코드 작성 및 실행

### 시나리오 3: 학습 분석 및 개인화된 학습 경로
1. 학습 분석 탭으로 이동
2. 학습 타임라인 확인
3. 맞춤형 추천 학습 경로 확인
4. 획득한 업적 확인

## 주요 기능 시연
- 사용자 프로필 기반 개인화된 응답
- 학습 이력 추적 및 시각화
- 코드 실습 환경
- 맞춤형 학습 경로 추천
- 게이미피케이션 요소 (업적 시스템)

## 알림
이 데모는 실제 백엔드 시스템과 연결되어 있지 않으며, 미리 정의된 시나리오를 시연하기 위한 목적으로 만들어졌습니다.
실제 구현 시 MongoDB, FastAPI, LangChain, OpenAI API 등의 기술을 활용하여 완전한 기능을 구현할 수 있습니다. 
