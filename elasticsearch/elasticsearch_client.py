from elasticsearch import Elasticsearch
import json
import logging

# Config du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ElasticsearchClient:
    def __init__(self, hosts=["http://localhost:9200"], index_name="default_index"):
        """
        Initialise le client Elasticsearch.

        :param hosts: Liste des hôtes Elasticsearch.
        :param index_name: Index par défaut.
        """
        self.es = Elasticsearch(hosts)
        self.index_name = index_name
        if self.es.ping():
            logging.info("Connexion réussie  à ElasticSearch.")
        else:
            logging.error("Connexion Impossible à Elasticsearch.")
            raise ConnectionError("Connexion Impossible à Elasticsearch.")

    def create_index(self, mapping):
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, body=mapping)
                logging.info(f"L'index '{self.index_name}' a été créé avec succès.")
            else:
                 logging.info(f"L'index '{self.index_name}' existe déjà.")
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'index: {e}")
            raise

    def delete_index(self):
        
        try:
            if self.es.indices.exists(index=self.index_name):
                self.es.indices.delete(index=self.index_name)
                logging.info(f"L'index '{self.index_name}' a été supprimé.")
            else:
                logging.info(f"L'index '{self.index_name}' n'existe pas.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'index: {e}")
            raise

    def index_document(self, document, document_id=None):
       
        try:
            res = self.es.index(index=self.index_name, body=document, id=document_id)
            logging.info(f"Document indexé avec l'ID '{res['_id']}'.")
            return res['_id']  
        except Exception as e:
            logging.error(f"Erreur lors de l'indexation du document: {e}")
            raise

    def search(self, query):
       
        try:
            response = self.es.search(index=self.index_name, body=query)
            return response
        except Exception as e:
            logging.error(f"Erreur lors de la recherche: {e}")
            raise

    def refresh_index(self):
       
        try:
            self.es.indices.refresh(index=self.index_name)
            logging.info(f"L'index '{self.index_name}' a été rafraîchi.")
        except Exception as e:
            logging.error(f"Erreur lors du rafraîchissement de l'index: {e}")
            raise

    def get_document(self, document_id):
        
        try:
            response = self.es.get(index=self.index_name, id=document_id)
            return response['_source']
        except Exception as e:
            logging.warning(f"Document avec l'ID '{document_id}' non trouvé ou erreur: {e}")
            return None

    def update_document(self, document_id, document):
       
        try:
            self.es.update(index=self.index_name, id=document_id, body={"doc": document})
            logging.info(f"Document avec l'ID '{document_id}' mis à jour.")
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour du document '{document_id}': {e}")
            raise

    def delete_document(self, document_id):
       
        try:
            self.es.delete(index=self.index_name, id=document_id)
            logging.info(f"Document avec l'ID '{document_id}' supprimé.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du document '{document_id}': {e}")
            raise