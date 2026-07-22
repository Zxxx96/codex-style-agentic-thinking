"""Login flow. User records are keyed by normalized email (see registration.py)."""


def login(users: dict, email: str, password: str) -> bool:
    email = email.strip()
    user = users.get(email)
    if user is None:
        return False
    return user["password"] == password
