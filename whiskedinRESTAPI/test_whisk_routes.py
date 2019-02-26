import unittest

import bcrypt

from whiskedinRESTAPI.app import db, app, User


class UserTests(unittest.TestCase):
    TEST_DB = 'test.db'

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_get_user_empty(self):
        username = 'username'
        user = User.get_user(username)
        self.assertEqual(None, user)

    def test_get_user_exists(self):
        user_to_add = User(username='username', hashed_password='password')
        db.session.add(user_to_add)
        db.session.commit()
        user = User.get_user('username')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.hashed_password, 'password')

    def test_create_user(self):
        user = User.create_user('username', 'password')
        self.assertIsInstance(user, User)
        created_user = User.query.filter_by(username='username').first()
        self.assertEqual(created_user.username, user.username)
        self.assertEqual(created_user.hashed_password, user.hashed_password)

    def test_register(self):
        response = self.app.post('/register', data={'username': 'username', 'password': 'password'})
        self.assertEqual(response.status, '201 CREATED')
        self.assertIn('access_token', response.json)

    def test_login_no_user(self):
        response = self.app.post('/login', data={'username': 'username', 'password': 'password'})
        self.assertEqual(response.status, '400 BAD REQUEST')
        self.assertIn('msg', response.json)

    def test_login_user_exists(self):
        password = 'password'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username='username', hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        response = self.app.post('/login', data={'username': 'username', 'password': 'password'})
        self.assertEqual(response.status, '200 OK')
        self.assertIn('access_token', response.json)
