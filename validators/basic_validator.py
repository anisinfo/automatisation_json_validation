import json

class BasicValidator:
    @staticmethod
    def is_valid_json(json_str):
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False
    
    @staticmethod
    def validate_user(data):
        if not isinstance(data, dict):
            raise ValueError("Les données doivent être un dictionnaire")
        if 'nom' not in data:
            raise ValueError("Le champ 'nom' est requis")
        if 'age' not in data:
            raise ValueError("Le champ 'age' est requis")
        if not isinstance(data['nom'], str):
            raise ValueError("Le nom doit être une chaîne de caractères")
        if not isinstance(data['age'], int):
            raise ValueError("L'âge doit être un entier")
        if data['age'] < 0:
            raise ValueError("L'âge ne peut pas être négatif")
        return True