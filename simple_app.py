import streamlit as st

# App configuration
st.set_page_config(
    page_title="CodeMate - 코딩 AI 튜터 데모",
    page_icon="🤖",
    layout="wide"
)

# Main content
st.title("🤖 CodeMate - AI 코딩 튜터 데모")

st.write("---")

st.subheader("🚀 배포 성공!")
st.write("CodeMate 데모 앱이 성공적으로 배포되었습니다.")

# Sample login form
with st.container():
    st.subheader("로그인")
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("아이디", value="user123")
    
    with col2:
        st.text_input("비밀번호", type="password", value="demo1234")
    
    st.button("로그인")

st.write("---")

# Footer
st.caption("© 2025 코드메이트 - 개인화된 AI 코딩 튜터")
