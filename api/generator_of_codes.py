import secrets

def generate_code(length=8):
    """Generate a secure random code of the specified length."""
    api_code = secrets.token_urlsafe(64)
    return api_code