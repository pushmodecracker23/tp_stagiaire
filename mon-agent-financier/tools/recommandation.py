CATALOGUE = [
    {
        "id": 1,
        "nom": "Laptop Pro 15\"",
        "categorie": "Informatique",
        "prix": 1299.99,
        "description": "Ordinateur portable haute performance, idéal pour les professionnels",
        "compte_recommande": ["Premium", "VIP"],
    },
    {
        "id": 2,
        "nom": "Souris ergonomique sans fil",
        "categorie": "Informatique",
        "prix": 49.99,
        "description": "Souris confortable pour une utilisation prolongée",
        "compte_recommande": ["Standard", "Premium", "VIP"],
    },
    {
        "id": 3,
        "nom": "Bureau standing électrique",
        "categorie": "Mobilier",
        "prix": 799.00,
        "description": "Bureau réglable en hauteur pour un travail sain",
        "compte_recommande": ["Premium", "VIP"],
    },
    {
        "id": 4,
        "nom": "Chaise de bureau ergonomique",
        "categorie": "Mobilier",
        "prix": 349.00,
        "description": "Chaise confortable avec support lombaire ajustable",
        "compte_recommande": ["Standard", "Premium", "VIP"],
    },
    {
        "id": 5,
        "nom": "Casque audio premium",
        "categorie": "Audio",
        "prix": 249.99,
        "description": "Casque sans fil avec réduction de bruit active",
        "compte_recommande": ["Premium", "VIP"],
    },
    {
        "id": 6,
        "nom": "Enceinte Bluetooth portable",
        "categorie": "Audio",
        "prix": 89.99,
        "description": "Enceinte compacte avec 12h d'autonomie",
        "compte_recommande": ["Standard", "Premium", "VIP"],
    },
]


def recommander_produits(input_str: str) -> str:
    """Recommande des produits adaptés au budget, à la catégorie et au type de compte client.
    Format d'entrée : 'budget,categorie,type_compte' ex: '500,Informatique,Premium'.
    Catégories disponibles : Informatique, Mobilier, Audio, Toutes.
    Types de compte : Standard, Premium, VIP.
    """
    try:
        parts = input_str.strip().split(",")
        if len(parts) != 3:
            return (
                "Erreur : format attendu 'budget,categorie,type_compte' "
                "ex: '500,Informatique,Premium'"
            )

        budget = float(parts[0].strip())
        categorie = parts[1].strip()
        type_compte = parts[2].strip()

        produits_filtres = []
        for produit in CATALOGUE:
            if produit["prix"] > budget:
                continue
            if categorie.lower() not in ("toutes", "all", "") and \
               produit["categorie"].lower() != categorie.lower():
                continue
            if type_compte not in produit["compte_recommande"]:
                continue
            produits_filtres.append(produit)

        if not produits_filtres:
            return (
                f"Aucun produit trouvé pour :\n"
                f"  Budget : {budget:.2f}€\n"
                f"  Catégorie : {categorie}\n"
                f"  Type de compte : {type_compte}\n"
                f"Essayez d'augmenter votre budget ou de changer de catégorie."
            )

        produits_filtres.sort(key=lambda p: p["prix"], reverse=True)

        output = (
            f"Recommandations pour un client {type_compte} "
            f"(budget : {budget:.2f}€, catégorie : {categorie}) :\n"
        )
        for p in produits_filtres:
            output += (
                f"\n  [{p['categorie']}] {p['nom']}\n"
                f"    Prix        : {p['prix']:.2f}€\n"
                f"    Description : {p['description']}\n"
            )
        return output.strip()

    except ValueError:
        return "Erreur : le budget doit être un nombre valide."
    except Exception as e:
        return f"Erreur inattendue : {e}"
