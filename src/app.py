import streamlit as st
from ask import answer

st.set_page_config(page_title="AI Paper Assistant", page_icon="📚")
st.title("📚 AI Research Paper Assistant")
st.caption("Ask questions about 8 famous AI papers. Answers come only from the papers.")

# Chat history (kept while the page is open)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat box at the bottom
question = st.chat_input("Ask about the papers...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the papers..."):
            r = answer(question)

        if r["blocked"]:
            st.warning("🛡️ " + r["text"])
        else:
            st.markdown(r["text"])
            with st.expander("📄 Sources"):
                for s in r["sources"]:
                    name = s["uri"].split("/")[-1] or "unknown"
                    st.markdown(f"**[{s['n']}] {name}** — score {s['score']:.2f}")
                    st.caption(s["text"][:300] + "...")

    st.session_state.messages.append({"role": "assistant", "content": r["text"]})