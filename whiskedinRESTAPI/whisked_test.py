import os
import unittest

import bcrypt
from flask_jwt_extended import JWTManager

from whiskedinRESTAPI.whiskedinRESTAPI.app import db, app, User


class WhiskedTest(unittest.TestCase):

    TEST_DB = 'test.db'

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.user = self.create_test_user()

    def create_test_user(self, username='username'):
        password = 'password'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user
