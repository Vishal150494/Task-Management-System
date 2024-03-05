#tests/test_user_model.py
import unittest
from flask_testing import TestCase
from src.task_management.auth.models import User
from src.task_management.db import db
from src.main import create_web_app

class TestUserModel(TestCase):
    def create_app(self):
        """Standard in-built flask function; Test to setup the Web app with test config"""
        return create_web_app()
    
    def setUp(self):
        """Special Test Methods (in-built) to set up testing environment before testing is started"""
        # Creates all db table for User model
        db.create_all()

    def tearDown(self):
        """Special Test Methods (in-built) to clean up test enviroments after all tests are completed"""
        db.session.remove()
        db.drop_all()
        
    def test_user_password(self):
        """Test to check if password storing / hashing methods"""
        user = User(username='Vishal', email_id='test_id@testing.com')
        user.create_password('testing_password')
        self.assertFalse(user.password == 'testing_password')
        self.assertTrue(user.check_password('testing_password'))
        self.assertFalse(user.check_password('development_password'))
        
    def test_user_representation(self):
        """Test to check username & email-id representation"""
        user = User(username='Vishal Ashok', email_id='test_id@testing.com')
        user.create_password('testing_password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(repr(user), f"<User Vishal Ashok:test_id@testing.com>")
        
if __name__ == '__main__':
    unittest.main()
        