# Agent Financier Intelligent (Claude)

Agent conversationnel financier basé sur LangGraph / LangChain et Anthropic **Claude 3.5 Haiku**, capable d'interroger une base de données MySQL, d'effectuer des calculs financiers, de consulter des cours boursiers et de recommander des produits.

## Prérequis

- Python 3.10+
- Docker & Docker Compose
- Une clé API Anthropic

## Installation

### 1. Configurer l'environnement

```bash
cd mon-agent-financier

# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env et renseigner votre clé Anthropic
# ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 3. Démarrer la base de données MySQL

```bash
docker-compose up -d
```

Attendez ~15 secondes que MySQL soit prêt, puis vérifiez :

```bash
docker-compose ps
```

### 4. Lancer l'agent

```bash
python main.py
```

## Utilisation

Au démarrage, un menu interactif propose 5 scénarios prédéfinis ou la saisie libre :

```
============================================================
     AGENT FINANCIER CLAUDE - Menu Principal
============================================================

Scénarios prédéfinis :
  1. Recherche client et recommandation produits
  2. Cours boursier et conversion de devise
  3. Calcul de prêt immobilier
  4. Analyse d'un investissement avec intérêts composés
  5. Cours crypto et marge commerciale
  6. Saisir une question libre
  0. Quitter
```

## Architecture

```
mon-agent-financier/
├── agent.py              # Graphe ReAct LangGraph + MemorySaver
├── main.py               # Interface interactive
├── tools/
│   ├── database.py       # MySQL : rechercher_client / rechercher_produit (@tool)
│   ├── finance.py        # Cours actions & crypto simulés (@tool)
│   ├── calculs.py        # TVA, intérêts composés, marge, mensualité (@tool)
│   ├── api_publique.py   # Conversion devises — API Frankfurter réelle (@tool)
│   └── recommandation.py # Catalogue 6 produits / 3 catégories (@tool)
├── docker-compose.yml    # MySQL 8, port 3306, init automatique
├── init.sql              # 3 clients FR + 5 produits
├── requirements.txt
├── .env.example
└── README.md
```

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| LLM | Anthropic Claude 3.5 Haiku (`claude-3-5-haiku-20241022`) |
| Agent | `create_react_agent` (LangGraph) |
| Exécution outils | `ToolNode` (LangGraph) |
| Mémoire | `MemorySaver` — persistance en mémoire par thread |
| Décorateur outils | `@tool` de `langchain_core.tools` |
| Base de données | MySQL 8 via `mysql-connector-python` |
| Taux de change | API Frankfurter (`api.frankfurter.app`) |

## Outils disponibles

| Outil | Description | Format d'entrée |
|-------|-------------|-----------------|
| `rechercher_client` | Recherche client en BDD | nom ou ID |
| `rechercher_produit` | Recherche produit en BDD | nom ou ID |
| `obtenir_cours_action` | Cours boursier simulé | symbole (AAPL, MSFT…) |
| `obtenir_cours_crypto` | Cours crypto simulé | symbole (BTC, ETH…) |
| `calculer_tva` | Calcul TVA + TTC | `prix_ht,taux` |
| `calculer_interets_composes` | Intérêts composés | `capital,taux,années` |
| `calculer_marge` | Marge commerciale | `prix_vente,cout_achat` |
| `calculer_mensualite_pret` | Mensualité de prêt | `capital,taux_annuel,mois` |
| `convertir_devise` | Conversion devises (réelle) | `montant,FROM,TO` |
| `recommander_produits` | Recommandation catalogue | `budget,categorie,type_compte` |

## Base de données

### Table `client`
| Nom | Solde | Type |
|-----|-------|------|
| Marie Dupont | 15 234,50 € | Standard |
| Jean-Pierre Martin | 87 650,00 € | Premium |
| Sophie Leclerc | 250 000,00 € | VIP |

### Table `product`
| Nom | Prix | Stock |
|-----|------|-------|
| Laptop Pro 15" | 1 299,99 € | 12 |
| Souris ergonomique sans fil | 49,99 € | 45 |
| Bureau standing électrique | 799,00 € | 8 |
| Chaise de bureau ergonomique | 349,00 € | 20 |
| Casque audio premium | 249,99 € | 30 |

## Arrêter la base de données

```bash
docker-compose down
# Pour supprimer aussi les données :
docker-compose down -v
```
