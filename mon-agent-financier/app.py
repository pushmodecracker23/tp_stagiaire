import uuid
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Agent Financier Claude",
    page_icon="💰",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Initialisation de la session (une seule fois par onglet navigateur)
# ---------------------------------------------------------------------------
if "agent" not in st.session_state:
    from agent import creer_agent
    st.session_state.agent = creer_agent()
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []  # [{"role": "user"|"assistant", "content": str}]

from agent import interroger_agent, TOOLS  # noqa: E402 — importé après init session


# ---------------------------------------------------------------------------
# Barre latérale — liste des outils disponibles + bouton reset
# ---------------------------------------------------------------------------
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
    st.caption("Modèle : Claude 3.5 Haiku")
    st.caption("Framework : LangGraph ReAct")

# ---------------------------------------------------------------------------
# Zone principale — historique du chat
# ---------------------------------------------------------------------------
st.title("💰 Agent Financier Claude")
st.caption("Posez vos questions sur les marchés, vos clients, vos calculs financiers…")

# Affichage de l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Message de bienvenue si la conversation est vide
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

# ---------------------------------------------------------------------------
# Champ de saisie (affiché en bas par Streamlit)
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Posez votre question financière…"):
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("ANTHROPIC_API_KEY manquante. Vérifiez votre fichier .env")
        st.stop()

    # Afficher et enregistrer le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Interroger l'agent et afficher la réponse
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours…"):
            response = interroger_agent(
                st.session_state.agent,
                prompt,
                thread_id=st.session_state.thread_id,
            )
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
