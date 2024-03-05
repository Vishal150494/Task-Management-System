#tests/test_task_model.py
import unittest
from datetime import datetime, timedelta
from flask_testing import TestCase
from src.task_management.auth.models import User
from src.task_management.tasks.models import Task
from src.task_management.db import db
from src.main import create_web_app

class TestTaskModel(TestCase):
    def create_app(self):
        """Standard in-built flask function; Test to setup the Web app with test config"""
        return create_web_app()
    
    def setUp(self):
        """Special Test Methods (in-built) to set up testing environment before testing is started"""
        # Creates all db table for User model
        db.create_all()
        user = User(username='Vishal', email_id='test_id@testing.com')
        user.create_password('testing_password')
        db.session.add(user)
        db.session.commit()
        
    def tearDown(self):
        """Special Test Methods (in-built) to clean up test enviroments after all tests are completed"""
        db.session.remove()
        db.drop_all()
        
    def test_task_creation(self):
        """Test to check actual task creation process"""
        user = User.query.first()
        title = 'Test Task Management Web Application'
        description = 'Test the Web App in order to containerize & deploy'
        due_date = datetime.utcnow() + timedelta(days=1)
        priority = 'High'
        status = 'In Progress'
        assignee = user.id
        created_on = datetime.utcnow()
        task = Task(title=title, 
                    description=description, 
                    due_date=due_date, 
                    priority=priority, 
                    status=status, 
                    assignee=assignee, 
                    created_on=created_on)
        db.session.add(task)
        db.session.commit()
        self.assertEqual(Task.query.count(), 1)
        self.assertEqual(task.title, title)
        self.assertEqual(task.assignee, assignee)
        
if __name__ == '__main__':
    unittest.main()