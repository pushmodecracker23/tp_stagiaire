import mysql.connector
from mysql.connector import Error
from langchain_core.tools import tool


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        database="db",
        user="user",
        password="password"
    )


@tool
def rechercher_client(query: str) -> str:
    """Recherche un client dans la base de données par nom ou identifiant.
    Entrée : le nom ou l'identifiant du client à rechercher.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id, name, balance, account_type FROM client WHERE name LIKE %s OR id LIKE %s"
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return f"Aucun client trouvé pour la recherche : '{query}'"

        output = f"Clients trouvés pour '{query}' :\n"
        for row in results:
            output += (
                f"- ID: {row['id']} | Nom: {row['name']} | "
                f"Solde: {row['balance']}€ | Type: {row['account_type']}\n"
            )
        return output.strip()

    except Error as e:
        return f"Erreur de base de données : {e}"


@tool
def rechercher_produit(query: str) -> str:
    """Recherche un produit dans la base de données par nom ou identifiant.
    Entrée : le nom ou l'identifiant du produit à rechercher.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id, name, price, stock FROM product WHERE name LIKE %s OR id LIKE %s"
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return f"Aucun produit trouvé pour la recherche : '{query}'"

        output = f"Produits trouvés pour '{query}' :\n"
        for row in results:
            output += (
                f"- ID: {row['id']} | Nom: {row['name']} | "
                f"Prix: {row['price']}€ | Stock: {row['stock']} unités\n"
            )
        return output.strip()

    except Error as e:
        return f"Erreur de base de données : {e}"
