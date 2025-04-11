from elasticsearch import Elasticsearch
import json
import logging
from elasticsearch.elasticsearch_client import ElasticsearchClient  # Import de la classe

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Configuration Elasticsearch
INDEX_NAME = "poc_recherche_alertes"
es_client = ElasticsearchClient(index_name=INDEX_NAME)

# 2. Mapping de l'index
mapping = {
    "mappings": {
        "properties": {
            "titre": {"type": "text", "analyzer": "french"},
            "contenu": {"type": "text", "analyzer": "french"},
            "auteur": {"type": "keyword"},
            "date_publication": {"type": "date"},
            "severite": {"type": "keyword"}
        }
    }
}

# 3. Création de l'index (si inexistant)
try:
    es_client.delete_index() #Suppression de l'index existant
    es_client.create_index(mapping)
except Exception as e:
    logging.error(f"Erreur lors de la création/suppression de l'index: {e}")
    exit()

# 4. Insertion de documents (Alertes Zabbix)
documents = [
    {
        "titre": "Zabbix: CPU trop élevée sur Serveur Web",
        "contenu": "L'utilisation du CPU sur le serveur web a dépassé 90%. Veuillez vérifier immédiatement.",
        "auteur": "Zabbix",
        "date_publication": "2024-12-11",
        "severite": "Critique"
    },
    {
        "titre": "Zabbix: Espace disque faible sur la base de données",
        "contenu": "L'espace disque disponible sur le serveur de base de données est inférieur à 10%.",
        "auteur": "Zabbix",
        "date_publication": "2024-12-11",
        "severite": "Avertissement"
    },
    {
        "titre": "Zabbix: Serveur DNS injoignable",
        "contenu": "Le serveur DNS principal est injoignable depuis plus de 5 minutes.",
        "auteur": "Zabbix",
        "date_publication": "2024-12-11",
        "severite": "Critique"
    }
]

try:
    for doc in documents:
        es_client.index_document(doc)
    es_client.refresh_index()
    logging.info(f"{len(documents)} documents Zabbix indexés.")
except Exception as e:
    logging.error(f"Erreur lors de l'indexation des documents Zabbix: {e}")

# 5. Exemples de requêtes
query_simple = {
    "query": {
        "match": {
            "contenu": "CPU"
        }
    }
}

query_severite = {
    "query": {
        "bool": {
            "must": [
                {"match": {"auteur": "Zabbix"}}
            ],
            "filter": [
                {"term": {"severite": "Critique"}}
            ]
        }
    }
}

query_fulltext = {
    "query": {
        "multi_match": {
            "query": "disque base de données",
            "fields": ["titre", "contenu"],
            "type": "best_fields"
        }
    }
}

# 6. Affichage des résultats (factorisation)
def afficher_resultats(reponse):
    hits = reponse['hits']['hits']
    print(f"Nombre de résultats : {len(hits)}")
    for hit in hits:
        print(f"\nID: {hit['_id']}")
        print(f"Score: {hit['_score']}")
        print(f"Source: {json.dumps(hit['_source'], indent=2, ensure_ascii=False)}")

# 7. Exécution des recherches et affichage
try:
    print("\n=== Recherche simple (CPU) ===")
    resultats_simple = es_client.search(query_simple)
    afficher_resultats(resultats_simple)

    print("\n=== Recherche par sévérité (Critique) ===")
    resultats_severite = es_client.search(query_severite)
    afficher_resultats(resultats_severite)

    print("\n=== Recherche full-text (disque base de données) ===")
    resultats_fulltext = es_client.search(query_fulltext)
    afficher_resultats(resultats_fulltext)

except Exception as e:
    logging.error(f"Erreur lors de l'exécution des requêtes: {e}")