import unittest

from evaluation import Evaluation


class TestRequests(unittest.TestCase):
    session = Evaluation(error=None)

    def test_login(self):
        flag, message = self.session.login_request(username='1651312', password='cjh1998CJH', code='1234')
        self.assertFalse(flag)

    def test_get_verification_code_image(self):
        flag, image, message = self.session.get_verification_code_image()
        self.assertTrue(flag)


if __name__ == '__main__':
    unittest.main()
