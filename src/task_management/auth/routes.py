#src/task_management/auth/routes.py
"""
This module handles authentication routes for the task management application.
It supports registering new users, logging in, and logging out.
"""
from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from src.task_management.db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    """This method registers user in the backend on the data base"""
    print(request.form)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email_id')
        
        if not username or not password or not email:
            return jsonify({"error":"Required fields missing from the form"}), 400  
    
        existing_user = User.query.filter((User.username == username) | (User.email_id == email)).first()
    
        if existing_user: 
            """Checking 'user' db table if an entry with the provided 'username' already exists."""
            return jsonify({"error":"User already registered. Please try to sign in"}), 400
        
        hash_password = generate_password_hash(password)
        new_user = User(username=username, email_id=email, password=hash_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("User registered successfully.")
            return redirect(url_for('auth.login')) #201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Registration failed"}), 500
    return render_template('register.html')
    
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    """This method authenticates a user based on his/her user/login credentials"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('tasks.dashboard'))
        else:
            return jsonify({"message":"Invalid user credentials. Please try again"}), 401
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """This method discards/invalidates the session token created in 'login' method and logs out the user"""
    logout_user()
    flash("You have been loged out.", 'info')
    return redirect(url_for('auth.login')) #200
