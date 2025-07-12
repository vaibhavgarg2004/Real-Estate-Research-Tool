import streamlit as st
from rag import process_urls, generate_answer

st.set_page_config(page_title="Real Estate Research Tool", layout="centered")
st.markdown("""
    <style>
        .main-title { font-size: 40px; font-weight: 700; text-align: center; color: #2c3e50; }
        .sub-header { font-size: 18px; font-weight: 600; color: #34495e; }
        .source-link { font-size: 16px; color: #2980b9; }
        .answer-box {
            background-color: #2d3436;
            color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            font-size: 17px;
            line-height: 1.6;
        }
        .source-link a {
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏘️ Real Estate Research Tool</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar inputs
st.sidebar.header("🔗 Enter Article URLs")
url1 = st.sidebar.text_input("URL 1")
url2 = st.sidebar.text_input("URL 2")
url3 = st.sidebar.text_input("URL 3")

st.sidebar.markdown("---")
process_url_button = st.sidebar.button("🚀 Process URLs")

# Placeholder for feedback
placeholder = st.empty()

# Handle URL Processing
if process_url_button:
    urls = [url for url in (url1, url2, url3) if url.strip()]
    if not urls:
        st.sidebar.warning("⚠️ You must provide at least one valid URL.")
    else:
        progress = st.progress(0, text="Initializing...")
        for i, status in enumerate(process_urls(urls)):
            progress.progress((i + 1) / 7, text=status)  
        progress.empty()
        st.session_state["urls_processed"] = True 
    if st.session_state.get("urls_processed"):
        st.success("✅ URLs processed successfully.")

st.markdown("## Ask a Question")
query = st.text_input("💬 Enter your question here")

if query:
    try:
        with st.spinner("Generating answer..."):
            answer, sources = generate_answer(query)

        st.markdown("### 🧠 Answer")
        st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

        if sources:
            st.markdown("### 📄 Sources")
            for source in sources.split("\n"):
                if source.strip():
                    st.markdown(f'<div class="source-link">🔗 <a href="{source}" target="_blank">{source}</a></div>', unsafe_allow_html=True)
    except RuntimeError:
        st.error("⚠️ You must process URLs first.")
