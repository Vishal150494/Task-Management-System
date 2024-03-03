#src/task_management/tasks/routes.py
"""
This module handles task management routes for the task management application.
It supports adding, viewing, editing, deleting .... tasks.
"""
from flask import Blueprint, request, jsonify, flash, redirect, render_template, url_for
from flask_login import login_required, logout_user, current_user
from .models import Task
from src.task_management.db import db

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """This method simply displays the dashboard with all tasks list"""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

@task_bp.route('/add_task', methods=['GET','POST'])
@login_required
def add_new_task():
    """This method handles adding / creating new tasks"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority'] 
        assignee = request.form['assignee']
        
        new_task = Task(title=title, description=description, due_date=due_date, priority=priority, assignee=assignee)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message":"New task added successfully."}), 201
    return render_template('add_task.html')

@task_bp.route('/edit_task/<int:task_id>', methods=['GET','POST'])
@login_required
def edit_task(task_id):
    """This method handles all task editing functions, like editing description, title, ....."""
    task = Task.query.get_or_404(task_id, "Task not found in the database")
    
    if task.assignee != current_user.id:
        #return jsonify({"mesage":"User not authorized"}), 401
        flash("User not authorized to edit this task", "FAILED!")
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.due_date = request.form['due_date']
        task.priority = request.form['priority']
        task.assignee = request.form['assignee']
        
        db.session.commit()
        flash("Task updated successfully!", "SUCCESS")
        return redirect(url_for('dashboard'))
    return render_template('edit_task.html', task=task)
        
@task_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """This method deletes task from the dashboard"""
    task = Task.query.get_or_404(task_id, "Task not found in the database")
    
    if task.assignee != current_user.id:
        flash("User not authorized to delete this task", "FAILED!")
        return redirect(url_for('dashboard'))
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message":"Task deleted successfully from the dashboard"}), 201

        