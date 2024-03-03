#src/task_management/tasks/models.py
"""
This model is used to represent fields for task management,
like due date, priority, assignees and so on.
"""
from ..db import db
from datetime import datetime

class Task(db.Model):
    """
    Task model for storing information related to the tasks
    """
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(50), nullable=False, default="Low") # Low, Normal, High
    status = db.Column(db.String(50), nullable=False, default="To Do") # To Do, Review, In Progress, Done
    assignee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        """
        Standard python Method to return a string representation of the task object that includes the title of the task.
        """
        return f"<Task {self.title}>"
    