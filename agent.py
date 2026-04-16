import os
from langchain_openai import ChatOpenAI
from langchain_classic.tools import Tool
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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
    _python_repl,
]


def creer_agent() -> AgentExecutor:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant financier précis. Utilise les outils disponibles pour répondre aux questions."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    agent = create_openai_tools_agent(llm=llm, tools=TOOLS, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
    )

    return agent_executor


def interroger_agent(agent: AgentExecutor, question: str, thread_id: str = None) -> str:
    try:
        result = agent.invoke({"input": question})
        return result.get("output", "L'agent n'a pas retourné de réponse.")
    except Exception as e:
        return f"Erreur lors de l'interrogation de l'agent : {e}"
