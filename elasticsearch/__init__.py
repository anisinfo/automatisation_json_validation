from elasticsearch import Elasticsearch
from datetime import datetime
import json

# 1. Connexion à Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

# 2. Nom de l'index
INDEX_NAME = "poc_recherche_alertes"

# 3. Suppression de l'index s'il existe déjà (pour repartir de zéro)
if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)

# 4. Création d'un index avec un mapping personnalisé
mapping = {
    "mappings": {
        "properties": {
            "titre": {"type": "text", "analyzer": "french"},
            "contenu": {"type": "text", "analyzer": "french"},
            "auteur": {"type": "keyword"},  # Pas d'analyse pour les filtres exacts
            "date_publication": {"type": "date"},
            "nb_vues": {"type": "integer"},
            "severite": {"type": "keyword"}  # Ajout du champ "severite"
        }
    }
}
es.indices.create(index=INDEX_NAME, body=mapping)

# 5. Insertion de quelques documents (Alertes Zabbix)
documents = [
    {
        "titre": "Test de recherche avec Elasticsearch",
        "contenu": "Elasticsearch est un moteur de recherche distribué.",
        "auteur": "Anis",
        "date_publication": "2024-12-11",
        "nb_vues": 1500
    },
    {
        "titre": "Recherche avancée avec Python",
        "contenu": "Comment utiliser Elasticsearch en Python pour des requêtes complexes.",
        "auteur": "Emmanuel",
        "date_publication": "2024-12-11",
        "nb_vues": 800
    },
    {
        "titre": "Data Science et Elasticsearch",
        "contenu": "Utiliser Elasticsearch pour l'analyse de données en temps réel.",
        "auteur": "Anis",
        "date_publication": "2024-12-11",
        "nb_vues": 1200
    }
]

for i, doc in enumerate(documents):
    es.index(index=INDEX_NAME, id=i+1, body=doc)

# Rafraîchir l'index pour que les données soient disponibles pour la recherche
es.indices.refresh(index=INDEX_NAME)

# 6. Exemples de requêtes de recherche

# Requête 1 : Recherche simple (match sur "contenu")
query_simple = {
    "query": {
        "match": {
            "contenu": "Python"
        }
    }
}

# Requête 2 : Recherche avec filtres (auteur + date)
query_filtree = {
    "query": {
        "bool": {
            "must": [
                {"match": {"auteur": "Anis"}}
            ],
            "filter": [
                {"range": {"date_publication": {"gte": "2023-10-01"}}}
            ]
        }
    }
}

# Requête 3 : Recherche full-text avec scoring (boost sur le titre)
query_boost = {
    "query": {
        "multi_match": {
            "query": "recherche données",
            "fields": ["titre^3", "contenu"],  # ^3 = boost x3 pour le titre
            "type": "best_fields"
        }
    }
}

# 7. Exécution des requêtes et affichage des résultats
def afficher_resultats(reponse):
    hits = reponse['hits']['hits']
    print(f"Nombre de résultats : {len(hits)}")
    for hit in hits:
        print(f"\nID: {hit['_id']}")
        print(f"Score: {hit['_score']}")
        print(f"Source: {json.dumps(hit['_source'], indent=2, ensure_ascii=False)}")

print("\n=== Résultats : Recherche simple (Python) ===")
resultats_simple = es.search(index=INDEX_NAME, body=query_simple)
afficher_resultats(resultats_simple)

print("\n=== Résultats : Recherche filtrée (Anis après Octobre 2023) ===")
resultats_filtree = es.search(index=INDEX_NAME, body=query_filtree)
afficher_resultats(resultats_filtree)

print("\n=== Résultats : Recherche boostée (titre prioritaire) ===")
resultats_boost = es.search(index=INDEX_NAME, body=query_boost)
afficher_resultats(resultats_boost)