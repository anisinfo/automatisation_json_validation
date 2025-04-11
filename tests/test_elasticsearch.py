import unittest
from unittest.mock import MagicMock, patch
from elasticsearch.elasticsearch_client import ElasticsearchClient

class TestElasticsearchClient(unittest.TestCase):

    @patch('elasticsearch.Elasticsearch')
    def setUp(self, MockElasticsearch):
        self.mock_es = MockElasticsearch.return_value
        self.index_name = "test_index"
        self.es_client = ElasticsearchClient(index_name=self.index_name)

    def test_create_index(self):
        mapping = {
            "mappings": {
                "properties": {
                    "field1": {"type": "text"},
                    "field2": {"type": "keyword"}
                }
            }
        }
        self.es_client.create_index(mapping)
        self.mock_es.indices.create.assert_called_once_with(index=self.index_name, body=mapping)

    def test_delete_index(self):
        self.es_client.delete_index()
        self.mock_es.indices.delete.assert_called_once_with(index=self.index_name)

    def test_index_document(self):
        document = {"field1": "value1", "field2": "value2"}
        self.es_client.index_document(document)
        self.mock_es.index.assert_called_once_with(index=self.index_name, body=document)

    def test_search(self):
        query = {"query": {"match_all": {}}}
        self.es_client.search(query)
        self.mock_es.search.assert_called_once_with(index=self.index_name, body=query)

    def test_refresh_index(self):
        self.es_client.refresh_index()
        self.mock_es.indices.refresh.assert_called_once_with(index=self.index_name)

    def test_get_document(self):
        document_id = "1"
        self.es_client.get_document(document_id)
        self.mock_es.get.assert_called_once_with(index=self.index_name, id=document_id)

    def test_update_document(self):
        document_id = "1"
        document = {"field1": "new_value1"}
        self.es_client.update_document(document_id, document)
        self.mock_es.update.assert_called_once_with(index=self.index_name, id=document_id, body={"doc": document})

    def test_delete_document(self):
        document_id = "1"
        self.es_client.delete_document(document_id)
        self.mock_es.delete.assert_called_once_with(index=self.index_name, id=document_id)

if __name__ == '__main__':
    unittest.main()