import unittest
from access_management.account_authenticator import AccountAuthenticator

class TestAccountAuthenticator(unittest.TestCase):
    def setUp(self):
        self.authenticator = AccountAuthenticator()

    def test_authenticate_valid_credentials(self):
        result = self.authenticator.authenticate('valid_user', 'valid_password')
        self.assertTrue(result)

    def test_authenticate_invalid_credentials(self):
        result = self.authenticator.authenticate('invalid_user', 'invalid_password')
        self.assertFalse(result)

    def test_authenticate_empty_username(self):
        result = self.authenticator.authenticate('', 'some_password')
        self.assertFalse(result)

    def test_authenticate_empty_password(self):
        result = self.authenticator.authenticate('some_user', '')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
