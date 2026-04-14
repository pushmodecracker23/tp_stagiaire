from langchain_community.tools.tavily_search import TavilySearchResults

# Outil de recherche web spécialisé pour l'actualité financière
recherche_tavily = TavilySearchResults(
    max_results=5,
    description=(
        "Répond à des questions ouvertes sur l'actualité financière, les entreprises, "
        "les cours récents. Utilise cet outil pour toute question nécessitant des "
        "informations récentes non disponibles via les autres outils."
    ),
)
