import uuid

def generate_unique_code(length=8):
    """Generate a unique alphanumeric code of specified length."""
    return str(uuid.uuid4())[:length].upper()