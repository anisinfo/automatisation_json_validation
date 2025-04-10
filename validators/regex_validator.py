import re

class RegexValidator:
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone):
        pattern = r'^(\+33|0)[1-9][0-9]{8}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_postal_code(code):
        pattern = r'^[0-9]{5}$'
        return bool(re.match(pattern, code))