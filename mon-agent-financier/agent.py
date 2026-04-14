import uuid
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.checkpoint.memory import MemorySaver

# ATTENTION SECURITE : PythonREPLTool exécute du code arbitraire.
# Ne jamais utiliser en production sans sandbox.
from langchain_experimental.tools import PythonREPLTool

from tools.database import rechercher_client, rechercher_produit
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.calculs import (
    calculer_tva,
    calculer_interets_composes,
    calculer_marge,
    calculer_mensualite_pret,
)
from tools.api_publique import convertir_devise
from tools.recommandation import recommander_produits
from tools.portefeuille import get_networth
from tools.tavily import recherche_tavily

# Identifiant de session unique pour la mémoire conversationnelle (CLI)
SESSION_THREAD_ID = str(uuid.uuid4())

# PythonREPLTool — exécution de code Python arbitraire pour calculs avancés
_python_repl = PythonREPLTool()
_python_repl.description = (
    "Exécute du code Python pour des calculs complexes non couverts par les autres outils. "
    "Entrée : code Python valide."
)

TOOLS = [
    rechercher_client,
    rechercher_produit,
    obtenir_cours_action,
    obtenir_cours_crypto,
    calculer_tva,
    calculer_interets_composes,
    calculer_marge,
    calculer_mensualite_pret,
    convertir_devise,
    recommander_produits,
    get_networth,
    recherche_tavily,
    _python_repl,
]


def creer_agent():
    """Crée et retourne un agent ReAct LangGraph avec mémoire conversationnelle."""
    llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)

    # ToolNode gère l'exécution des appels d'outils dans le graphe LangGraph
    tool_node = ToolNode(TOOLS)  # noqa: F841 — utilisé implicitement par create_react_agent

    memory = MemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=TOOLS,
        checkpointer=memory,
    )

    return agent


def interroger_agent(agent, question: str, thread_id: str = None) -> str:
    """Envoie une question à l'agent et retourne sa réponse textuelle.

    Args:
        agent: L'AgentExecutor LangGraph créé par creer_agent().
        question: La question à poser à l'agent.
        thread_id: Identifiant de thread pour la mémoire. Utilise SESSION_THREAD_ID si None.
    """
    tid = thread_id if thread_id is not None else SESSION_THREAD_ID
    config = {"configurable": {"thread_id": tid}}
    try:
        result = agent.invoke(
            {"messages": [("human", question)]},
            config=config,
        )
        messages = result.get("messages", [])
        if messages:
            last = messages[-1]
            # Compatibilité : content peut être une liste de blocs (Anthropic) ou une chaîne
            content = last.content
            if isinstance(content, list):
                texts = [
                    block.get("text", "") if isinstance(block, dict) else str(block)
                    for block in content
                ]
                return "\n".join(t for t in texts if t).strip()
            return str(content).strip()
        return "L'agent n'a pas retourné de réponse."
    except Exception as e:
        return f"Erreur lors de l'interrogation de l'agent : {e}"
