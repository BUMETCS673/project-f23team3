import unittest
from flask import session
from flask_testing import TestCase
from app import app, db
from Models import *
from CloudOP import register_with_email, login_with_email
from DataOP import get_orders_from_staff, find_name_from_id, clear_cart
from unittest.mock import patch
import json
from random import randint

class AdvancedTests(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'testing'
        return app

    def setUp(self):
        db.create_all()
        self.populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_db(self):
        # 使用随机或每次测试都不同的 id 值
        random_id = str(randint(1000, 9999))
        customer = Customer(id=random_id, name="Jane Doe", email="jane@example.com")
        db.session.add(customer)
        db.session.commit()

    # 测试用户注册
    def test_user_registration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                inputName="Test User",
                inputEmail="testuser3@example.com",
                inputPassword="password"
            ), follow_redirects=True)
            self.assertIn(b'Success, please verify your email address before login.', response.data)

    # 测试用户登录
    def test_user_login(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                inputEmail="testuser@example.com",
                inputPassword="password"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            # 检查是否重定向到了正确的页面
            self.assertIn('/menu', response.request.path)
    # 测试清空购物车
    def test_clear_cart(self):
        with self.client:
            clear_cart(1)  # 假设表ID为1
            # 进一步检查购物车是否清空

    # 测试数据库模型
    def test_order_model(self):
        order = Order(id=1, status="pending")
        db.session.add(order)
        db.session.commit()
        self.assertEqual(order.status, "pending")

    # 测试 Firebase 集成
    @patch('CloudOP.requests.post')
    def test_firebase_integration(self, mock_post):
        mock_post.return_value.json.return_value = {
            "localId": "testId",
            "email": "test@example.com"
        }
        response = register_with_email("test@example.com", "password")
        self.assertEqual(response['email'], "test@example.com")

    # 测试特定路由的响应
    def test_specific_route(self):
        response = self.client.get('/some_route')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
