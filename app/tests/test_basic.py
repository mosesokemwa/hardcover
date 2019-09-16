import os
import unittest

from app import app, models, db


TEST_DB = 'test.db'
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(PROJECT_DIR, TEST_DB)

        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
        # mail.init_app(app)
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(fname='moses', lname='moses', email=email,
                      password=password, password2=password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def authenticated_user(self):
        self.register('okemwamoses@gmail.com',
                      'FlaskIsAwesome', 'FlaskIsAwesome')
        self.login(email='okemwamoses@gmail.com', password='FlaskIsAwesome')

    def test_add_item_to_cart(self):
        self.authenticated_user()
        response = self.app.post('/addToCart',
                                 query_string={
                                     "productId": '1',
                                     'quantity': '3'
                                 },
                                 follow_redirects=True
                                 )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item successfully added to cart !!', response.data)

    def test_add_invalid_item_to_cart(self):
        self.authenticated_user()
        response = self.app.post('/addToCart',
                                 query_string={
                                     "productId": '1',
                                     'quantity': '3'
                                 },
                                 follow_redirects=True
                                 )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item successfully added to cart !!', response.data)

    def test_delete_item_from_cart(self):
        self.authenticated_user()
        response = self.app.post('/addToCart',
                                 query_string={
                                     "productId": '1',
                                     'quantity': '3'
                                 },
                                 follow_redirects=True
                                 )
        response = self.app.post('/removeFromCart',
                                 query_string={
                                     "productId": '1'
                                 },
                                 follow_redirects=True
                                 )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product has been removed from cart !!', response.data)
