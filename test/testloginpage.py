import unittest
from app import app, db

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        # Setting up the test environment
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Clean up the environment
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page(self):
        # Test GET request
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login', response.get_data(as_text=True))



if __name__ == '__main__':
    unittest.main()
