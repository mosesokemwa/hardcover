from app.models import User
import os
import unittest

from app import app, models, db


TEST_DB = 'test.db'
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


class UsersTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
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

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

###############
#### tests ####
###############

    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_valid_user_registration(self):
        response = self.register('moses@gmail.com',
                                 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Congratulations, you are now a registered user!', response.data)

    def test_invalid_user_registration_different_passwords(self):
        response = self.register('okemwamoses@gmail.com',
                                 'FlaskIsAwesome', 'FlaskIsNotAwesome.')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('okemwamoses@gmail.com', '', 'FlaskIsAwesome')
        self.assertIn(b'This field is required.', response.data)

    def test_invalid_user_registration_duplicate_email(self):
        response = self.register('okemwamoses@gmail.com',
                                 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        response = self.register('okemwamoses@gmail.com',
                                 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
        self.assertIn(b'Please use a different email address.', response.data)

    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Click to Register!', response.data)
        self.assertIn(b'Sign In', response.data)

    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('okemwamoses@gmail.com',
                      'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/logout', follow_redirects=True)
        self.app.get('/login', follow_redirects=True)
        response = self.login('okemwamoses@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'okemwamoses@gmail.com', response.data)

if __name__ == "__main__":
    unittest.main()
