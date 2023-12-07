import unittest
import sys
sys.path.insert(0, '../')
from flask import Flask, url_for
from flask_testing import TestCase
from selenium import webdriver
from app import app, db
from Models import DishType, Dish


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

    def test_DishType_route(self):
        test_main_dish = DishType(id=1, name='Test main dish', description='Test description')
        db.session.add(test_main_dish)
        db.session.commit()

    def test_dish_customer_index(self):
        test_dish = Dish(id=1, general_dish_id=1, name='Test main dish', cost=5, description='Test description')
        db.session.add(test_dish)
        db.session.commit()

        self.driver = webdriver.Chrome()
        url = url_for('dishes_customer_index', general_dish_id=1)
        self.driver.get(url)

        main_dish_name_element = self.driver.find_element_by_id('mainDishName')
        self.assertEqual(main_dish_name_element.text, 'Test Main Dish')


if __name__ == '__main__':
    unittest.main()
