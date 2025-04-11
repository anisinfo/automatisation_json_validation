import pytest
from validators.schema_validator import SchemaValidator

class TestSchemaValidator:
    def test_valid_user_schema(self):
        data = {"titre": "Test Alerte", "contenu": "Alerte de test", "auteur": "Zabbix", "date_publication": "2024-12-11", "severite": "Information"}
        assert SchemaValidator.validate_alerte(data) is True
    
    def test_invalid_user_schema(self):
        with pytest.raises(ValueError):
            SchemaValidator.validate_alerte({"titre": "", "contenu": "Alerte de test", "auteur": "Zabbix", "date_publication": "2024-12-11", "severite": "Information"})