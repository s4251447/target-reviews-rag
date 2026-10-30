import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Target Reviews Chatbot", page_icon="🎯")
st.title("🎯 Target Reviews Chatbot")
st.caption("Ask a question and I'll answer using customer reviews.")

TEMPLATE = """
You are an expert in answering questions about a Retail Store (Target).
Answer using only the reviews below. If they don't cover the question, say you don't know.

Here are some relevant reviews:
{reviews}

Here is the question to answer: {question}
"""


# Streamlit reruns this whole script on every interaction, so load the heavy
# stuff once and cache it. Importing vector.py builds/loads the Chroma DB.
@st.cache_resource(show_spinner="Loading reviews database (first run can take a minute)...")
def load_chain():
    from vector import retriever

    model = OllamaLLM(model="llama3.2")
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    return retriever, prompt | model


retriever, chain = load_chain()


def format_reviews(docs):
    return "\n".join(
        f"- (Rating: {d.metadata.get('rating')}, Date: {d.metadata.get('date')}) {d.page_content}"
        for d in docs
    )


def show_sources(docs):
    with st.expander(f"Reviews used ({len(docs)})"):
        for d in docs:
            st.markdown(f"**Rating:** {d.metadata.get('rating')}  |  **Date:** {d.metadata.get('date')}")
            st.write(d.page_content)
            st.divider()


# Sidebar
with st.sidebar:
    st.header("Options")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Chat history lives in session_state so it survives reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("docs"):
            show_sources(msg["docs"])

# Replaces the input() loop from main.py
if question := st.chat_input("Ask about Target..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            docs = retriever.invoke(question)
            answer = st.write_stream(
                chain.stream({"reviews": format_reviews(docs), "question": question})
            )
            show_sources(docs)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "docs": docs}
            )
        except Exception as e:
            st.error(f"Something went wrong. Is Ollama running?\n\n{e}")