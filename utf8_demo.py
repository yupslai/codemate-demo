import streamlit as st

# App configuration
st.set_page_config(
    page_title="CodeMate - 코딩 AI 튜터 데모",
    page_icon="🤖",
    layout="wide"
)

# Main content
st.title("🤖 CodeMate - AI 코딩 튜터 데모")

st.markdown("---")

# Login form
with st.container():
    st.subheader("로그인")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_id = st.text_input("사용자 ID:", value="user123", 
                               placeholder="사용자 ID를 입력하세요")
    
    with col2:
        password = st.text_input("비밀번호:", value="demo1234", 
                                type="password", 
                                placeholder="비밀번호를 입력하세요")
    
    login_btn = st.button("로그인", help="데모 계정: user123 / demo1234")
    
    if login_btn:
        st.success("로그인 성공! 간단한 데모 버전입니다.")
        st.balloons()

# Sample content
st.markdown("---")
st.subheader("📚 코드메이트는 무엇인가요?")
st.write("""
CodeMate는 7-16세 학생들을 위한 AI 코딩 튜터입니다. 
학생의 관심사와 배경지식에 맞춘 개인화된 코딩 교육을 제공합니다.

주요 기능:
- 학생의 관심사 기반 코딩 설명 (예: 마인크래프트 예제)
- 대화형 코딩 학습 및 질문-답변
- 코드 디버깅 지원
- 실시간 피드백이 있는 실습 문제
- 학습 진행 상황 분석
""")

# Sample code
st.markdown("---")
st.subheader("💻 코드 예제")
code = '''
def place_blocks(block_type, count):
    # 블록을 놓는 함수
    for i in range(count):
        print(f"{block_type} 블록을 놓았습니다.")
        
    print(f"총 {count}개의 {block_type} 블록을 놓았습니다. 완료!")
    
# 함수 테스트
place_blocks("돌", 5)
'''
st.code(code, language="python")

# Footer
st.markdown("---")
st.caption("© 2025 코드메이트 - 개인화된 AI 코딩 튜터")
