import unittest
import sys
sys.path.insert(0, '../')
from app import app, db
from Models import Orders, Customers, Dining_tables, Staffs


class OrderManagementTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # 添加一些测试数据
        customer = Customers(id="1", preferred_name="John Doe", email="john@example.com")
        staff = Staffs(id="1", first_name="Jane", last_name="Doe", email="jane@example.com", role="Server", status="Active")
        dining_table = Dining_tables(id=1, server_id=staff.id, status="Available", capacity=4)
        order = Orders(id=1, table_id=dining_table.id, customer_id=customer.id, date="2021-01-01", status="Pending", payment=100, requests="No onions")
        db.session.add_all([customer, staff, dining_table, order])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_view_order_details(self):
        response = self.client.get('/order_details/1')
        self.assertEqual(response.status_code, 200)
        # 检查响应中是否包含特定的订单信息
        self.assertIn("No onions", response.get_data(as_text=True))

    def test_update_order_status(self):
        response = self.client.post('/update_order_status/1', data={'status': 'Completed'})
        self.assertEqual(response.status_code, 200)  # 或其他预期的响应码
        updated_order = Orders.query.get(1)
        self.assertEqual(updated_order.status, 'Completed')

if __name__ == '__main__':
    unittest.main()
