import streamlit as st
from utils.components import set_page, render_navbar, render_footer, section_header

set_page("AI Assistant", "💬")
render_navbar(active="AI Assistant")

section_header(
    "Ask anything",
    "AI Pregnancy Assistant",
    "Ask a pregnancy-related question. This assistant provides educational "
    "information only.",
)

# FAQ content unchanged from the original app
faq = {

    "is headache normal":
    """Mild headaches can occur during pregnancy due to hormonal changes.

🚨 Seek medical attention if the headache is severe, persistent, or accompanied by blurred vision or swelling.""",

    "can i exercise":
    """Light exercise such as walking or prenatal yoga is generally safe for most pregnancies.

Always consult your healthcare provider before starting any exercise program.""",

    "what should i eat":
    """A healthy pregnancy diet should include:

• Fruits
• Vegetables
• Whole grains
• Lean protein
• Dairy products
• Plenty of water""",

    "can i drink coffee":
    """Yes, but caffeine intake should be limited.

Most healthcare guidelines recommend keeping caffeine below 200 mg per day during pregnancy.""",

    "is nausea normal":
    """Morning sickness is common, especially during the first trimester.

If vomiting becomes severe or prevents eating and drinking, consult your healthcare provider.""",

    "when should i go to the doctor":
    """Seek immediate medical care if you experience:

• Heavy vaginal bleeding
• Severe abdominal pain
• Loss of fetal movement
• High fever
• Severe headache with blurred vision""",

    "can i travel":
    """Travel is generally considered safe during uncomplicated pregnancies.

Discuss travel plans with your healthcare provider, especially during the third trimester.""",

    "what vitamins should i take":
    """Prenatal vitamins commonly include:

• Folic Acid
• Iron
• Calcium
• Vitamin D

Only take supplements recommended by your healthcare provider."""
}

FALLBACK = (
    "I don't have enough information.\n\n"
    "Please consult your healthcare provider for personalized medical advice."
)


def answer(question: str) -> str:
    """Identical matching logic to the original rule-based assistant."""
    for key in faq:
        if key in question.lower():
            return faq[key]
    return FALLBACK


# -----------------------------
# Chat history
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "Hi! 👋 I'm your pregnancy assistant. Ask me about symptoms, "
            "nutrition, exercise, or anything else on your mind.",
        }
    ]

with st.container(key="glass_step"):
    for msg in st.session_state.chat_history:
        avatar = "🤰" if msg["role"] == "assistant" else "🙂"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    # Suggested questions
    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    suggestions = [
        "Is headache normal?",
        "Can I exercise?",
        "What should I eat?",
        "Can I drink coffee?",
    ]
    chip_cols = st.columns(len(suggestions))
    for i, q in enumerate(suggestions):
        with chip_cols[i]:
            with st.container(key=f"ghostbtn7_{i}"):
                if st.button(q, key=f"chip_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer(q)}
                    )
                    st.rerun()

question = st.chat_input("Ask your question…")

if question:
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer(question)}
        )
        st.rerun()

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

with st.expander("📋 Example Questions"):
    st.markdown("""
- Is headache normal?
- Can I exercise?
- What should I eat?
- Can I drink coffee?
- Is nausea normal?
- When should I go to the doctor?
- Can I travel?
- What vitamins should I take?
""")

st.caption(
    "Educational purposes only. This assistant is not a substitute for professional medical advice."
)

render_footer()
