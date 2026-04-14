import requests
from langchain_core.tools import tool


@tool
def convertir_devise(input_str: str) -> str:
    """Convertit un montant d'une devise à une autre via l'API Frankfurter (taux de change réels).
    Format d'entrée : 'montant,FROM,TO' ex: '100,EUR,USD'.
    Devises supportées : EUR, USD, GBP, JPY, CHF, CAD, AUD, et bien d'autres.
    """
    try:
        parts = input_str.strip().split(",")
        if len(parts) != 3:
            return "Erreur : format attendu 'montant,FROM,TO' ex: '100,EUR,USD'"

        montant = float(parts[0].strip())
        from_currency = parts[1].strip().upper()
        to_currency = parts[2].strip().upper()

        url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return f"Erreur API : impossible d'obtenir le taux de change ({response.status_code})"

        data = response.json()

        if to_currency not in data.get("rates", {}):
            return (
                f"Erreur : devise '{to_currency}' non disponible. "
                f"Devises supportées : EUR, USD, GBP, JPY, CHF, CAD, AUD..."
            )

        taux = data["rates"][to_currency]
        montant_converti = round(montant * taux, 2)
        date_taux = data.get("date", "inconnue")

        return (
            f"Conversion de devises :\n"
            f"  Montant initial  : {montant:.2f} {from_currency}\n"
            f"  Taux de change   : 1 {from_currency} = {taux} {to_currency}\n"
            f"  Montant converti : {montant_converti:.2f} {to_currency}\n"
            f"  Date du taux     : {date_taux}"
        )

    except requests.exceptions.ConnectionError:
        return "Erreur : impossible de se connecter à l'API Frankfurter. Vérifiez votre connexion internet."
    except requests.exceptions.Timeout:
        return "Erreur : l'API Frankfurter n'a pas répondu dans les délais."
    except ValueError:
        return "Erreur : le montant doit être un nombre valide."
    except Exception as e:
        return f"Erreur inattendue : {e}"
