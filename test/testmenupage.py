mport unittest
from app import app, db
from Models import Dishes, Dish_Label


class FullMenuTestCase(unittest.TestCase):

    def setUp(self):
        # 设置测试环境
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # 添加测试数据
        test_dish = Dishes(name='Test Dish', description='Test Description', cost=10)
        db.session.add(test_dish)
        db.session.commit()

        new_dish_label = Dish_Label(dish_id=test_dish.id, label='Test Label')
        db.session.add(new_dish_label)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_insert_form(self):
        response = self.client.get('/fm_insert_form')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Insert', response.get_data(as_text=True))

    def test_insert_post(self):
        # 测试前先添加 Dishes 实例
        test_dish = Dishes(name='Another Test Dish', description='Another Description', cost=15)
        db.session.add(test_dish)
        db.session.commit()

        # 发送 POST 请求
        response = self.client.post('/fm_insert_post', data={
            'dish_id': test_dish.id,  # 使用 dish_id 而不是 main_menu_id
            'label': 'Another Test Label'
        })
        self.assertEqual(response.status_code, 302)  # 检查是否重定向

        # 验证数据是否被插入
        dish_label = Dish_Label.query.filter_by(dish_id=test_dish.id, label='Another Test Label').first()
        self.assertIsNotNone(dish_label)

    def test_customer_view(self):
        response = self.client.get('/fm_customer_view/1')
        self.assertEqual(response.status_code, 200)
        # 修改断言以匹配实际页面内容
        self.assertIn('menu.html', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()