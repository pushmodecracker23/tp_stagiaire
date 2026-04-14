import os
from dotenv import load_dotenv
from agent import creer_agent, interroger_agent

load_dotenv()

SCENARIOS = [
    {
        "titre": "Recherche client et recommandation produits",
        "question": (
            "Recherche le client nommé 'Marie' et recommande-lui des produits "
            "dans la catégorie Informatique avec un budget de 800€."
        ),
    },
    {
        "titre": "Cours boursier et conversion de devise",
        "question": (
            "Quel est le cours actuel de l'action Apple (AAPL) ? "
            "Convertis également 500 USD en EUR."
        ),
    },
    {
        "titre": "Calcul de prêt immobilier",
        "question": (
            "Je souhaite emprunter 150 000€ sur 20 ans (240 mois) à un taux annuel de 3,5%. "
            "Calcule ma mensualité et le coût total du crédit."
        ),
    },
    {
        "titre": "Analyse d'un investissement avec intérêts composés",
        "question": (
            "Si j'investis 5 000€ à un taux annuel de 7% pendant 15 ans, "
            "combien aurai-je au bout de cette période ? "
            "Calcule aussi la TVA sur un produit à 299€ HT avec un taux de 20%."
        ),
    },
    {
        "titre": "Cours crypto et marge commerciale",
        "question": (
            "Donne-moi le cours du Bitcoin (BTC) et de l'Ethereum (ETH). "
            "Calcule aussi la marge si j'achète un produit 80€ et le revends 129€."
        ),
    },
]

# ---------------------------------------------------------------------------
# Scénario de démonstration de la mémoire conversationnelle (C2)
# ---------------------------------------------------------------------------
DEMO_MEMOIRE = [
    "Quel est le type de compte et le solde du client Marie ?",
    "Quel produit lui recommandes-tu ?",
    "Calcule le prix TTC et dis-moi si elle peut se le permettre.",
]


def demo_memoire(agent):
    """Lance les 3 questions en séquence pour démontrer la mémoire conversationnelle."""
    print("\n" + "=" * 60)
    print("  DÉMONSTRATION — Mémoire conversationnelle (3 questions)")
    print("=" * 60)
    print("L'agent conserve le contexte entre chaque question.\n")

    for i, question in enumerate(DEMO_MEMOIRE, 1):
        print(f"[Q{i}] {question}")
        print("-" * 60)
        reponse = interroger_agent(agent, question)
        print(f"[A{i}]\n{reponse}")
        print()
        input("Appuyez sur Entrée pour la question suivante...")


def afficher_menu(nb_scenarios: int):
    print("\n" + "=" * 60)
    print("     AGENT FINANCIER CLAUDE - Menu Principal")
    print("=" * 60)
    print("\nScénarios prédéfinis :")
    for i, scenario in enumerate(SCENARIOS, 1):
        print(f"  {i}. {scenario['titre']}")
    print(f"  {nb_scenarios + 1}. Démonstration mémoire conversationnelle")
    print(f"  {nb_scenarios + 2}. Saisir une question libre")
    print(f"  0. Quitter")
    print("-" * 60)


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERREUR : La variable ANTHROPIC_API_KEY n'est pas définie.")
        print("Créez un fichier .env avec ANTHROPIC_API_KEY=votre_clé")
        return

    print("\nInitialisation de l'agent financier Claude...")
    agent = creer_agent()
    print("Agent prêt !\n")

    nb_scenarios = len(SCENARIOS)

    while True:
        afficher_menu(nb_scenarios)

        try:
            choix = input("Votre choix : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nAu revoir !")
            break

        if choix == "0":
            print("\nAu revoir !")
            break

        elif choix.isdigit() and 1 <= int(choix) <= nb_scenarios:
            index = int(choix) - 1
            scenario = SCENARIOS[index]
            print(f"\n--- Scénario : {scenario['titre']} ---")
            print(f"Question : {scenario['question']}\n")
            reponse = interroger_agent(agent, scenario["question"])
            print("\n" + "=" * 60)
            print("RÉPONSE DE L'AGENT :")
            print("=" * 60)
            print(reponse)

        elif choix == str(nb_scenarios + 1):
            demo_memoire(agent)

        elif choix == str(nb_scenarios + 2):
            print("\nSaisissez votre question (ou 'retour' pour revenir au menu) :")
            try:
                question = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nAu revoir !")
                break

            if question.lower() in ("retour", "back", ""):
                continue

            reponse = interroger_agent(agent, question)
            print("\n" + "=" * 60)
            print("RÉPONSE DE L'AGENT :")
            print("=" * 60)
            print(reponse)

        else:
            print("\nChoix invalide, veuillez réessayer.")

        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
