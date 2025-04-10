from jsonschema import validate, ValidationError

class SchemaValidator:
    USER_SCHEMA = {
        "type": "object",
        "properties": {
            "nom": {"type": "string", "minLength": 1},
            "age": {"type": "integer", "minimum": 0},
            "email": {"type": "string", "format": "email"},
        },
        "required": ["nom", "age"],
        "additionalProperties": False
    }

    @classmethod
    def validate_user(cls, data):
        try:
            validate(instance=data, schema=cls.USER_SCHEMA)
            return True
        except ValidationError as e:
            raise ValueError(f"Erreur de validation: {e.message}")