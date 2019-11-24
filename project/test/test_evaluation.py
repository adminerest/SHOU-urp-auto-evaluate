import unittest

from evaluation import Evaluation


class MyTestCase(unittest.TestCase):
    session = Evaluation(error=None)

    def test_login(self):
        print(self.session.login_request(username='1651312', password='cjh1998CJH', code='1234'))

    def test_get_verification_code_image(self):
        print(self.session.get_verification_code_image())


if __name__ == '__main__':
    unittest.main()
