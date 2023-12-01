import unittest
from flask import Flask, url_for
from flask_testing import TestCase
from selenium import webdriver
from main import app, db
from model import main_dishes, dishes


class TestRoutes(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_dishes_route(self):
        test_main_dish = main_dishes(id=1, name='Test main dish', description='Test description')
        db.session.add(test_main_dish)
        db.session.commit()

    def test_dishes_customer_index(self):
        test_dishes = dishes(id=1, main_dish_id = 1, name='Test main dish',cost=5, description='Test description')
        db.session.add(test_dishes)
        db.session.commit()

        self.driver = webdriver.Chrome()
        url = url_for('menu_dishes.customer_index', main_dish_id=1)
        self.driver.get(url)

        main_dish_name_element = self.driver.find_element_by_id('mainDishName')
        self.assertEqual(main_dish_name_element.text, 'Test Main Dish')

if __name__ == '__main__':
    unittest.main()
