from tavily import TavilyClient
import os


def recherche_tavily(query: str) -> str:
    """Recherche des informations sur l'actualité financière, les entreprises et les marchés.
    Entrée : une question ou un sujet à rechercher.
    """
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(query=query, search_depth="basic")
        results = response.get("results", [])
        if not results:
            return "Aucun résultat trouvé."
        output = ""
        for r in results[:3]:
            output += f"- {r.get('title', '')}: {r.get('content', '')[:200]}\n"
        return output
    except Exception as e:
        return f"Erreur Tavily: {str(e)}"
