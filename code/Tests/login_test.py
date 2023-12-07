import unittest
import sys
sys.path.insert(0, '../')
from app import app, db


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        # 设置测试环境
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # 清理环境
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page(self):
        # 测试 GET 请求
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
