import pytest
from validators.schema_validator import SchemaValidator

class TestSchemaValidator:
    def test_valid_user_schema(self):
        data = {"nom": "Bob", "age": 30}
        assert SchemaValidator.validate_user(data) is True
    
    def test_invalid_user_schema(self):
        with pytest.raises(ValueError):
            SchemaValidator.validate_user({"nom": "", "age": 30})