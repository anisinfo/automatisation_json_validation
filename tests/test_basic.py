import pytest
from validators.basic_validator import BasicValidator

class TestBasicValidator:
    def test_valid_user(self):
        data = {"nom": "Anis", "age": 25}
        assert BasicValidator.validate_user(data) is True
    
    def test_invalid_user_missing_field(self):
        with pytest.raises(ValueError):
            BasicValidator.validate_user({"nom": "Anis"})
    
    def test_invalid_age(self):
        with pytest.raises(ValueError):
            BasicValidator.validate_user({"nom": "Anis", "age": -1})