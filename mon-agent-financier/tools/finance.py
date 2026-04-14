import yfinance as yf
from langchain_core.tools import tool


def _extraire_donnees_ticker(ticker_sym: str):
    """Retourne (prix, open_price, volume, currency) ou lève une ValueError."""
    ticker = yf.Ticker(ticker_sym)

    # fast_info est plus léger que .info pour les données temps-réel
    fast = ticker.fast_info
    prix = getattr(fast, "last_price", None)

    if not prix:
        info = ticker.info
        prix = info.get("currentPrice") or info.get("regularMarketPrice")
        if not prix:
            raise ValueError(f"Symbole '{ticker_sym}' introuvable ou marché fermé.")
        open_price = info.get("open") or info.get("regularMarketOpen", prix)
        volume = info.get("volume") or info.get("regularMarketVolume", 0)
        currency = info.get("currency", "USD")
    else:
        open_price = getattr(fast, "open", prix)
        volume = getattr(fast, "three_month_average_volume", 0) or 0
        currency = getattr(fast, "currency", "USD")

    return float(prix), float(open_price), int(volume), currency


@tool
def obtenir_cours_action(symbole: str) -> str:
    """Retourne le cours réel d'une action boursière via Yahoo Finance.
    Entrée : le symbole de l'action (ex: AAPL, MSFT, TSLA, GOOGL).
    """
    symbole = symbole.strip().upper()
    try:
        prix, open_price, volume, currency = _extraire_donnees_ticker(symbole)
        variation = round(prix - open_price, 2)
        variation_pct = round((variation / open_price) * 100, 2) if open_price else 0
        direction = "+" if variation >= 0 else ""
        return (
            f"Action {symbole} :\n"
            f"  Prix actuel    : {prix:.2f} {currency}\n"
            f"  Variation jour : {direction}{variation:.2f} ({direction}{variation_pct}%)\n"
            f"  Volume         : {volume:,}\n"
            f"  (données Yahoo Finance en temps réel)"
        )
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Erreur lors de la récupération du cours de '{symbole}' : {e}"


@tool
def obtenir_cours_crypto(symbole: str) -> str:
    """Retourne le cours réel d'une cryptomonnaie via Yahoo Finance.
    Entrée : le symbole de la crypto (ex: BTC, ETH, SOL, ADA) ou avec paire (ex: BTC-USD).
    """
    symbole = symbole.strip().upper()
    # Ajoute automatiquement -USD si aucune paire n'est précisée
    ticker_sym = symbole if "-" in symbole else f"{symbole}-USD"
    try:
        prix, open_price, volume, currency = _extraire_donnees_ticker(ticker_sym)
        variation = round(prix - open_price, 2)
        variation_pct = round((variation / open_price) * 100, 2) if open_price else 0
        direction = "+" if variation >= 0 else ""
        return (
            f"Cryptomonnaie {symbole} :\n"
            f"  Prix actuel    : {prix:.2f} {currency}\n"
            f"  Variation jour : {direction}{variation:.2f} ({direction}{variation_pct}%)\n"
            f"  Volume moyen   : {volume:,}\n"
            f"  (données Yahoo Finance en temps réel)"
        )
    except ValueError:
        return (
            f"Cryptomonnaie '{symbole}' introuvable. "
            f"Vérifiez le symbole (ex: BTC, ETH, SOL) ou ajoutez la paire (ex: BTC-EUR)."
        )
    except Exception as e:
        return f"Erreur lors de la récupération du cours de '{symbole}' : {e}"
