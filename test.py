import unittest
from password_generator import generate_password


class PasswordTestCase(unittest.TestCase):
    def test_type_one_password(self):
        res = generate_password(num_passwords=1)
        self.assertEqual(type(res), str)

    def test_type_three_passwords(self):
        res = generate_password(num_passwords=3)
        self.assertEqual(len(res), 3)

    def test_one_password(self):
        res = generate_password(num_passwords=1, length_password=20)
        self.assertEqual(len(res), 20)
        self.assertEqual(any(ch.isupper() for ch in res), True)
        self.assertEqual(any(ch.islower() for ch in res), True)
        self.assertEqual(any(ch.isdigit() for ch in res), True)
