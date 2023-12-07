import unittest
from app import app  
from Models import db, Cart, Dishes


class FlaskCartTestCase(unittest.TestCase):

    def setUp(self):
        # Setting up the test environment
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        # Push application context
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        # Clean the database
        db.session.remove()
        db.drop_all()
        # Remove the application context at the end of the test
        self.app_context.pop()

    def test_get_cart(self):
        # Test GET request
        response = self.app.get('/cart')
        self.assertEqual(response.status_code, 200)

    def test_post_cart(self):
        # Test POST request
        response = self.app.post('/cart', data={'dish_name': 'Pizza', 'quantity': '2'})
        self.assertEqual(response.status_code, 200)
        # Check the database for new shopping cart entries
        cart_item = Cart.query.filter_by(dish_id='Pizza').first()
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.quantity, 2)


if __name__ == '__main__':
    unittest.main()
