import uuid
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Agent Financier",
    page_icon="💰",
    layout="wide",
)

if "agent" not in st.session_state:
    from agent import creer_agent
    st.session_state.agent = creer_agent()
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []

from agent import interroger_agent, TOOLS

with st.sidebar:
    st.title("🛠️ Outils disponibles")
    st.caption(f"{len(TOOLS)} outils chargés")
    st.divider()

    for t in TOOLS:
        with st.expander(f"**{t.name}**"):
            st.caption(t.description or "Aucune description.")

    st.divider()

    if st.button("🔄 Réinitialiser la conversation", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.caption("Modèle : GPT-4o-mini")
    st.caption("Framework : LangChain")

st.title("💰 Agent Financier")
st.caption("Posez vos questions sur les marchés, vos clients, vos calculs financiers…")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Bonjour ! Je suis votre agent financier intelligent. Je peux vous aider à :\n\n"
            "- 🔍 **Rechercher** des clients et des produits\n"
            "- 📈 **Consulter** les cours d'actions et de cryptomonnaies en temps réel\n"
            "- 💱 **Convertir** des devises\n"
            "- 🧮 **Calculer** TVA, intérêts composés, mensualités de prêt, marges\n"
            "- 💼 **Évaluer** la valeur d'un portefeuille boursier\n"
            "- 🌐 **Rechercher** l'actualité financière\n\n"
            "Comment puis-je vous aider ?"
        )

if prompt := st.chat_input("Posez votre question financière…"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY manquante. Vérifiez votre fichier .env")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours…"):
            response = interroger_agent(
                st.session_state.agent,
                prompt,
                thread_id=st.session_state.thread_id,
            )
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
