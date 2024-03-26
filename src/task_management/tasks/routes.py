#src/task_management/tasks/routes.py
"""
This module handles task management routes for the task management application.
It supports adding, viewing, editing, deleting .... tasks.
"""
from datetime import datetime
from flask import Blueprint, request, jsonify, flash, redirect, render_template, url_for, make_response
from flask_login import login_required, logout_user, current_user
from .models import Task
from src.task_management.db import db

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """This method simply displays the dashboard with all tasks list"""
    tasks = Task.query.filter_by(assignee=current_user.id).all()
    response = make_response(render_template('dashboard.html', tasks=tasks))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@task_bp.route('/add_task', methods=['GET','POST'])
@login_required
def add_new_task():
    """This method handles adding / creating new tasks"""
    if request.method == 'POST':
        print(request.form)
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        priority = request.form.get('priority') 
        
        if not title or not due_date_str:
            flash("Error adding the task", "FAILED!")
            return redirect(url_for('tasks.dashboard')), 400
        
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            new_task = Task(title=title, description=description, due_date=due_date, priority=priority, assignee=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash("New task added successfully.", "SUCCESS")
            return redirect(url_for('tasks.dashboard')) #200
            #return render_template('add_task.html')
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding new task: {str(e)}", "FAILED!")
            return render_template('add_task.html')
    return render_template('add_task.html')

@task_bp.route('/edit_task/<int:task_id>', methods=['GET','POST'])
@login_required
def edit_task(task_id):
    """This method handles all task editing functions, like editing description, title, ....."""
    task = Task.query.get_or_404(task_id, "Task not found in the database")
    
    if request.method == 'POST':
        # Check for hidden _method field in the form
        if request.form.get('_method') == 'PUT':
            title = request.form.get('title')
            description = request.form.get('description')
            due_date_str = request.form.get('due_date')
            priority = request.form.get('priority')
        
            if not (title and due_date_str):
                flash("Title and Due Date cannot be empty.", "warning")
                return render_template('edit_task.html', task=task)
        
            try:
                task.title = title
                task.description = description
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                task.priority = priority
                db.session.commit()
                flash("Task updated successfully!", "success")
                return redirect(url_for('tasks.dashboard')) #302
            except Exception as e:
                db.session.rollback()
                flash(f"Error editing the task: {str(e)}", "error")
                return render_template('edit_task.html') #500

    return render_template('edit_task.html', task=task)
        
@task_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """This method deletes task from the dashboard"""
    task = Task.query.get_or_404(task_id, "Task not found in the database")
    
    try:
        db.session.delete(task)
        db.session.commit()
        message = "Task deleted successfully from the dashboard"
        if request.method == "DELETE":
            return jsonify({"message": message}), 200 # For API clients
    except Exception as e:
        message = f"Error deleting the task: {str(e)}"
        if request.method == 'DELETE':
            return jsonify({"error": message}), 500 #For API clients
    
    flash(message, "success" if request.method == 'POST' else "error")
    return redirect(url_for('tasks.dashboard')) # For web form submission
