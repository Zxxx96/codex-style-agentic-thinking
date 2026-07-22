"""Registration stores users keyed by normalized email."""

from src.validation import normalize_email


def register(users: dict, email: str, password: str) -> None:
    users[normalize_email(email)] = {"password": password}
