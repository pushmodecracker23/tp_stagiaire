import uuid
from langchain_anthropic import ChatAnthropic
from langchain_classic.tools import Tool
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
    Tool(
        name="rechercher_client",
        func=rechercher_client,
        description=(
            "Recherche un client dans la base de données MySQL par nom ou identifiant. "
            "Entrée : le nom ou l'ID du client à rechercher."
        ),
    ),
    Tool(
        name="rechercher_produit",
        func=rechercher_produit,
        description=(
            "Recherche un produit dans la base de données MySQL par nom ou identifiant. "
            "Entrée : le nom ou l'ID du produit à rechercher."
        ),
    ),
    Tool(
        name="obtenir_cours_action",
        func=obtenir_cours_action,
        description=(
            "Retourne le cours réel d'une action boursière via Yahoo Finance. "
            "Affiche le prix, la variation journalière et le volume. "
            "Entrée : le symbole boursier (ex: AAPL, MSFT, TSLA, GOOGL)."
        ),
    ),
    Tool(
        name="obtenir_cours_crypto",
        func=obtenir_cours_crypto,
        description=(
            "Retourne le cours réel d'une cryptomonnaie via Yahoo Finance. "
            "Entrée : le symbole de la crypto (ex: BTC, ETH, SOL) ou avec paire (ex: BTC-USD)."
        ),
    ),
    Tool(
        name="calculer_tva",
        func=calculer_tva,
        description=(
            "Calcule la TVA et le prix TTC à partir du prix HT. "
            "Entrée : 'prix_ht,taux' ex: '100,20' pour 100€ HT avec TVA à 20%."
        ),
    ),
    Tool(
        name="calculer_interets_composes",
        func=calculer_interets_composes,
        description=(
            "Calcule les intérêts composés d'un placement financier. "
            "Entrée : 'capital,taux,années' ex: '1000,5,10' pour 1000€ à 5% sur 10 ans."
        ),
    ),
    Tool(
        name="calculer_marge",
        func=calculer_marge,
        description=(
            "Calcule la marge commerciale entre un prix de vente et un coût d'achat. "
            "Entrée : 'prix_vente,cout_achat' ex: '150,100'."
        ),
    ),
    Tool(
        name="calculer_mensualite_pret",
        func=calculer_mensualite_pret,
        description=(
            "Calcule la mensualité d'un prêt bancaire et son coût total. "
            "Entrée : 'capital,taux_annuel,mois' ex: '10000,5,24' pour 10000€ à 5% sur 24 mois."
        ),
    ),
    Tool(
        name="convertir_devise",
        func=convertir_devise,
        description=(
            "Convertit un montant d'une devise à une autre via l'API Frankfurter (taux réels). "
            "Entrée : 'montant,FROM,TO' ex: '100,EUR,USD'."
        ),
    ),
    Tool(
        name="recommander_produits",
        func=recommander_produits,
        description=(
            "Recommande des produits selon le budget, la catégorie et le type de compte client. "
            "Entrée : 'budget,categorie,type_compte' ex: '500,Informatique,Premium'. "
            "Catégories : Informatique, Mobilier, Audio, Toutes. "
            "Types de compte : Standard, Premium, VIP."
        ),
    ),
    Tool(
        name="get_networth",
        func=get_networth,
        description=(
            "Calcule la valeur totale d'un portefeuille boursier avec les prix réels Yahoo Finance. "
            "Entrée : 'SYMBOLE:QUANTITE|SYMBOLE:QUANTITE' ex: 'AAPL:10|TSLA:5|MSFT:3'."
        ),
    ),
    Tool(
        name="recherche_tavily",
        func=recherche_tavily,
        description=(
            "Répond à des questions ouvertes sur l'actualité financière, les entreprises, "
            "les cours récents. Utilise cet outil pour toute question nécessitant des "
            "informations récentes non disponibles via les autres outils."
        ),
    ),
    _python_repl,      # PythonREPLTool est déjà un BaseTool
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
        agent: L'agent LangGraph créé par creer_agent().
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
