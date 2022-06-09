import secrets


def create_random_string_id():
    return secrets.token_hex(10)
