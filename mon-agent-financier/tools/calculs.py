def calculer_tva(input_str: str) -> str:
    """Calcule la TVA et le prix TTC à partir du prix HT.
    Format d'entrée : 'prix_ht,taux' ex: '100,20' pour 100€ HT avec TVA à 20%.
    """
    try:
        parts = input_str.strip().split(",")
        if len(parts) != 2:
            return "Erreur : format attendu 'prix_ht,taux' ex: '100,20'"
        prix_ht = float(parts[0].strip())
        taux = float(parts[1].strip())
        tva = round(prix_ht * taux / 100, 2)
        prix_ttc = round(prix_ht + tva, 2)
        return (
            f"Calcul TVA :\n"
            f"  Prix HT     : {prix_ht:.2f}€\n"
            f"  Taux TVA    : {taux}%\n"
            f"  Montant TVA : {tva:.2f}€\n"
            f"  Prix TTC    : {prix_ttc:.2f}€"
        )
    except ValueError:
        return "Erreur : les valeurs doivent être des nombres valides."


def calculer_interets_composes(input_str: str) -> str:
    """Calcule les intérêts composés d'un placement financier.
    Format d'entrée : 'capital,taux,années' ex: '1000,5,10' pour 1000€ à 5% sur 10 ans.
    """
    try:
        parts = input_str.strip().split(",")
        if len(parts) != 3:
            return "Erreur : format attendu 'capital,taux,années' ex: '1000,5,10'"
        capital = float(parts[0].strip())
        taux = float(parts[1].strip()) / 100
        annees = int(parts[2].strip())
        montant_final = round(capital * (1 + taux) ** annees, 2)
        interets = round(montant_final - capital, 2)
        return (
            f"Intérêts composés :\n"
            f"  Capital initial : {capital:.2f}€\n"
            f"  Taux annuel     : {taux * 100}%\n"
            f"  Durée           : {annees} ans\n"
            f"  Montant final   : {montant_final:.2f}€\n"
            f"  Intérêts gagnés : {interets:.2f}€"
        )
    except ValueError:
        return "Erreur : les valeurs doivent être des nombres valides."


def calculer_marge(input_str: str) -> str:
    """Calcule la marge commerciale entre un prix de vente et un coût d'achat.
    Format d'entrée : 'prix_vente,cout_achat' ex: '150,100'.
    """
    try:
        parts = input_str.strip().split(",")
        if len(parts) != 2:
            return "Erreur : format attendu 'prix_vente,cout_achat' ex: '150,100'"
        prix_vente = float(parts[0].strip())
        cout_achat = float(parts[1].strip())
        if prix_vente == 0:
            return "Erreur : le prix de vente ne peut pas être zéro."
        marge_brute = round(prix_vente - cout_achat, 2)
        taux_marge = round((marge_brute / prix_vente) * 100, 2)
        taux_marque = round((marge_brute / cout_achat) * 100, 2) if cout_achat != 0 else 0
        return (
            f"Calcul de marge :\n"
            f"  Prix de vente  : {prix_vente:.2f}€\n"
            f"  Coût d'achat   : {cout_achat:.2f}€\n"
            f"  Marge brute    : {marge_brute:.2f}€\n"
            f"  Taux de marge  : {taux_marge}%\n"
            f"  Taux de marque : {taux_marque}%"
        )
    except ValueError:
        return "Erreur : les valeurs doivent être des nombres valides."


def calculer_mensualite_pret(input_str: str) -> str:
    """Calcule la mensualité d'un prêt bancaire ainsi que son coût total.
    Format d'entrée : 'capital,taux_annuel,mois' ex: '10000,5,24' pour 10000€ à 5% sur 24 mois.
    """
    try:
        parts = input_str.strip().split(",")
        if len(parts) != 3:
            return "Erreur : format attendu 'capital,taux_annuel,mois' ex: '10000,5,24'"
        capital = float(parts[0].strip())
        taux_annuel = float(parts[1].strip()) / 100
        mois = int(parts[2].strip())
        taux_mensuel = taux_annuel / 12

        if taux_mensuel == 0:
            mensualite = round(capital / mois, 2)
        else:
            mensualite = round(
                capital * taux_mensuel / (1 - (1 + taux_mensuel) ** (-mois)), 2
            )

        cout_total = round(mensualite * mois, 2)
        cout_credit = round(cout_total - capital, 2)
        return (
            f"Mensualité de prêt :\n"
            f"  Capital emprunté  : {capital:.2f}€\n"
            f"  Taux annuel       : {taux_annuel * 100}%\n"
            f"  Durée             : {mois} mois\n"
            f"  Mensualité        : {mensualite:.2f}€\n"
            f"  Coût total        : {cout_total:.2f}€\n"
            f"  Coût du crédit    : {cout_credit:.2f}€"
        )
    except ValueError:
        return "Erreur : les valeurs doivent être des nombres valides."
