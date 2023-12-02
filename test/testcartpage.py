import unittest
from app import app  # 假设 CartPage.py 包含了 Flask 应用实例、数据库实例和 Cart 模型
from Models import db, Cart, Dishes


class FlaskCartTestCase(unittest.TestCase):

    def setUp(self):
        # 设置测试环境
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        # 推送应用上下文
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        # 清理数据库
        db.session.remove()
        db.drop_all()
        # 不要忘记在测试结束时删除应用上下文
        self.app_context.pop()

    def test_get_cart(self):
        # 测试 GET 请求
        response = self.app.get('/cart')
        self.assertEqual(response.status_code, 200)
        # 可以添加更多的断言来检查返回的内容

    def test_post_cart(self):
        # 测试 POST 请求
        response = self.app.post('/cart', data={'dish_name': 'Pizza', 'quantity': '2'})
        self.assertEqual(response.status_code, 200)
        # 检查数据库是否有新的购物车条目
        cart_item = Cart.query.filter_by(dish_id='Pizza').first()
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.quantity, 2)


if __name__ == '__main__':
    unittest.main()
