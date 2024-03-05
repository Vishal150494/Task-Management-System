#tests/test_auth_routes.py (integration test)
import unittest
from src.task_management.db import db
from src.main import create_web_app

class TestAuthIntegration(unittest.TestCase):
    def setUp(self):
        # Creates necessary tables in the database.
        self.app = create_web_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client() #Initializing a test client
            
    def tearDown(self):
        # Removes / drops the tables from the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
            
    def test_user_registration_and_login(self):
        """Test to check user registration & login functions"""
        #Simulating user registration
        response = self.client.post('/auth/register', data=dict(
            username='Vishal Ashok',
            email_id='test_id@testing.com',
            password='testing_password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        
        #Simulating user login
        response = self.client.post('/auth/login', data=dict(
            username='Vishal Ashok',
            password='testing_password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_register_existing_username(self):
        """Test to check already registered username. Negetive Testing"""
        # Registering a new user first
        self.client.post('/auth/register', data=dict(
            username='test_user',
            email_id='test@testing.com',
            password='testing'
        ), follow_redirects=True)
        
        #Trying to register the same user (↑) again
        response = self.client.post('/auth/register', data=dict(
            username='test_user',
            email_id='test@testing.com',
            password='testing'
        ), follow_redirects=True)
        self.assertIn("User already registered. Please try to sign in", response.data.decode('utf-8'))
    
    def test_login_incorrect_password(self):
        """Test to check a negetive scenario where in an incorrect password is provided"""
        #Registering a new user with valid credentials first
        self.client.post('/auth/register', data=dict(
            username='testuser',
            email_id='test@testing.com',
            password='test'
        ), follow_redirects=True)
        
        #Login for the same user (↑) but with incorrect password
        response = self.client.post('/auth/login', data=dict(
            username='testuser',
            password='wrongpassword',
        ), follow_redirects=True)
        self.assertIn('Invalid user credentials. Please try again', response.data.decode('utf-8'))
        
    def test_login_nonexisting_user(self):
        """Test to check a negetive scenario where in a non registered username is provided"""
        response = self.client.post('/auth/login', data=dict(
            username='wrongusername',
            password='test' 
        ), follow_redirects=True)
        self.assertIn('Invalid user credentials. Please try again', response.data.decode('utf-8'))
        
if __name__ == '__main__':
    unittest.main()
    