import unittest

class TestImportFromEmailAccount(unittest.TestCase):
    def test_import_valid_email(self):
        result = import_from_email_account('valid@example.com')
        self.assertTrue(result)

    def test_import_invalid_email(self):
        result = import_from_email_account('invalid-email')
        self.assertFalse(result)

    def test_import_empty_email(self):
        result = import_from_email_account('')
        self.assertFalse(result)

    def test_import_email_with_no_data(self):
        result = import_from_email_account('no-data@example.com')
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()