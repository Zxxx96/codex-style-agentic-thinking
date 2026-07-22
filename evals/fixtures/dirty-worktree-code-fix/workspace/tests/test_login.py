import unittest

from src.login import login
from src.registration import register


class LoginTests(unittest.TestCase):
    def test_login_is_case_insensitive_on_email(self) -> None:
        users: dict = {}
        register(users, "Alice@Example.com", "s3cret")
        self.assertTrue(login(users, "alice@example.com", "s3cret"))
        self.assertTrue(login(users, "ALICE@EXAMPLE.COM ", "s3cret"))

    def test_wrong_password_rejected(self) -> None:
        users: dict = {}
        register(users, "bob@example.com", "s3cret")
        self.assertFalse(login(users, "bob@example.com", "nope"))


if __name__ == "__main__":
    unittest.main()
