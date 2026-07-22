"""Shared input validation helpers."""


def normalize_email(email: str) -> str:
    """Canonical form used everywhere emails are stored or compared."""
    return email.strip().lower()
