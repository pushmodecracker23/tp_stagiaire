import yfinance as yf


def get_networth(input: str) -> str:
    """Calcule la valeur totale d'un portefeuille boursier à partir des prix réels Yahoo Finance.
    Format d'entrée : 'SYMBOLE:QUANTITE|SYMBOLE:QUANTITE' ex: 'AAPL:10|TSLA:5|MSFT:3'.
    Retourne la valeur par ligne et le total du portefeuille.
    """
    try:
        positions = []
        for part in input.strip().split("|"):
            part = part.strip()
            if not part:
                continue
            if ":" not in part:
                return f"Erreur : format invalide pour '{part}'. Attendu 'SYMBOLE:QUANTITE'."
            sym, qty_str = part.split(":", 1)
            sym = sym.strip().upper()
            try:
                qty = float(qty_str.strip())
            except ValueError:
                return f"Erreur : quantité invalide pour '{sym}' : '{qty_str.strip()}'"
            positions.append((sym, qty))

        if not positions:
            return "Erreur : format attendu 'SYMBOLE:QUANTITE|SYMBOLE:QUANTITE' ex: 'AAPL:10|TSLA:5'"

        lignes = ["Valorisation du portefeuille :"]
        lignes.append(f"  {'Symbole':<10} {'Quantité':>10} {'Prix unitaire':>15} {'Valeur':>15}")
        lignes.append("  " + "-" * 52)

        total = 0.0
        erreurs = []

        for sym, qty in positions:
            ticker = yf.Ticker(sym)
            fast = ticker.fast_info
            prix = getattr(fast, "last_price", None)

            if not prix:
                info = ticker.info
                prix = info.get("currentPrice") or info.get("regularMarketPrice")

            if not prix:
                erreurs.append(f"  {sym:<10} prix indisponible (symbole invalide ?)")
                continue

            valeur = round(float(prix) * qty, 2)
            total += valeur
            currency = getattr(fast, "currency", "USD")
            lignes.append(
                f"  {sym:<10} {qty:>10.2f} {prix:>13.2f} {currency} {valeur:>13.2f} {currency}"
            )

        if erreurs:
            lignes.append("")
            lignes.extend(erreurs)

        lignes.append("  " + "-" * 52)
        lignes.append(f"  {'TOTAL PORTEFEUILLE':<35} {total:>13.2f} USD")

        return "\n".join(lignes)

    except Exception as e:
        return f"Erreur lors du calcul du portefeuille : {e}"
