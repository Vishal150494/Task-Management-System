#tests/test_task_model.py
import unittest
from datetime import datetime, timedelta
from flask_testing import TestCase
from src.task_management.auth.models import User
from src.task_management.tasks.models import Task
from src.task_management.db import db
from src.main import create_web_app

class TestTaskCRUD(TestCase):
    def create_app(self):
        return create_web_app()
    
    def setUp(self):
        db.create_all()
        self.user = User(username='Vishal', email_id='testing@test.com')
        self.user.create_password('testing_password')
        self.user_1 = User(username='test', email_id='testing@testexample.com')
        self.user_1.create_password('testing')
        db.session.add(self.user)
        db.session.add(self.user_1)
        db.session.commit()
        
        #self.task = Task(title='Test Task', description='Test Description', due_date=datetime.utcnow() + timedelta(days=1), priority='High', assignee=self.user.id)
        #db.session.add(self.task)
        #db.session.commit()
        
        self.client.post('/auth/login', data=dict(
            username='Vishal',
            password='testing_password'
        ), follow_redirects=True)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_create_new_task(self):
        """Positive Test Case: Test to check creation of new task"""
        response = self.client.post('/tasks/add_task', data=dict(
            title='New task',
            description='Testing creation of new task',
            due_date=(datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d'),
            priority='High',
            assignee=self.user.id
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        
    def test_create_new_task_missing_field(self):
        """Negetive Test Case: Test to check task creation when title is not given"""
        response = self.client.post('/tasks/add_task', data=dict(
            title='',
            description='Testing creation of new task',
            due_date=(datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d'),
            priority='High',
            assignee=self.user.id
        ), follow_redirects=True)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 400)
        
    def test_edit_task(self):
        """Positive Test Case: Test to check editing of an already existing task"""
        # Adding a task before editing
        task = Task(
            title='Old Task',
            description="Old desc",
            due_date=(datetime.utcnow() + timedelta(days=1)),
            priority='High',
            assignee=self.user.id)
        
        db.session.add(task)
        db.session.commit()
        
        # Editing task
        response = self.client.post(f'/tasks/edit_task/{task.id}', data=dict(
            title='Edited Task',
            description='Edited Description',
            due_date=(datetime.utcnow() + timedelta(days=3)).strftime('%Y-%m-%d'),
            priority='Low',
            assignee=self.user.id
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        
        #Fetching the edited(UPDATED) task
        edited_task = Task.query.get(task.id)
        self.assertEqual(edited_task.title, 'Edited Task')
        self.assertEqual(edited_task.priority, 'Low')
        
    def test_delete_task(self):
        # Adding a task before deleting
        task = Task(
            title='Old Task',
            description="Old desc",
            due_date=(datetime.utcnow() + timedelta(days=1)),
            priority='High',
            assignee=self.user.id)
        
        db.session.add(task)
        db.session.commit()
        
        # Deleting task
        response = self.client.post(f'/tasks/delete_task/{task.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        
        # Fetching the deleted task
        deleted_task = Task.query.get(task.id)
        self.assertIsNone(deleted_task)
    
    def test_edit_nonexisting_task(self):
        """Negetive Test Scenario: Test to check task editing for a non-existing task"""
        response = self.client.post('/tasks/edit_task/9999', data=dict(
            title='Not Existing',
            description='The task is non existent',
            due_date=datetime.utcnow().strftime('%Y-%m-%d'),
            priority='Medium',
            assignee=self.user.id
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        
    def test_edit_task_wrong_user(self):
        """Negetive Test Scenario: Test to check task editing for another user by another user"""
        task = Task(
            title='Old Task',
            description="Old desc",
            due_date=(datetime.utcnow() + timedelta(days=1)),
            priority='High',
            assignee=self.user_1.id)
        
        db.session.add(task)
        db.session.commit()
        
        response = self.client.post(f'/tasks/edit_task/{task.id}', data=dict(
            title='Edited Task',
            description='Edited Description',
            due_date=(datetime.utcnow() + timedelta(days=3)).strftime('%Y-%m-%d'),
            priority='Low',
            assignee=self.user.id
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 403)
        
    def test_delete_task_unauthorized(self):
        """Negetive Test Scenario: Test to check delete task func but by an unauthorized user"""
        task = Task(
            title='Old Task',
            description="Old desc",
            due_date=(datetime.utcnow() + timedelta(days=1)),
            priority='High',
            assignee=self.user_1.id)
        
        db.session.add(task)
        db.session.commit()
        
        response = self.client.post(f"/tasks/delete_task/{task.id}", follow_redirects=True)
        self.assertEqual(response.status_code, 403)
        
if __name__ == '__main__':
    unittest.main()
        
    
        