import unittest
#from app import app, db
from views import *

class TestCartFunctionality(unittest.TestCase):

    # Test to check if delete function removes an item from the cart
    def test_delete_item_from_cart(self):

        # Add a dummy item to the cart
        dummy_item = Cart(user_id=1, dish_id=1, quantity=1, special="")
        db.session.add(dummy_item)
        db.session.commit()

        # Get the initial count of items in the cart
        initial_count = Cart.query.filter_by(user_id=1).count()

        # Perform the delete action
        delete(1)

        # Check if the item is removed from the cart
        updated_count = Cart.query.filter_by(user_id=1).count()
        self.assertEqual(updated_count, initial_count - 1)