#src/task_management/auth/routes.py
"""
This module handles authentication routes for the task management application.
It supports registering new users, logging in, and logging out.
"""
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from src.task_management.db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    """This method registers user in the backend on the data base"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email_id']
        
        if User.query.filter_by(username=username).first():
            """Checking 'user' db table if an entry with the provided 'username' already exists."""
            return jsonify({"error":"User already registered. Please try to sign in"}), 400
        
        hash_password = generate_password_hash(password)
        new_user = User(username=username, email_id=email, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"User registered successfully."}), 201
    return render_template('register.html')

@auth_bp.route('/dashboard')
def dashboard():
    """This method simply renders the dashboard view"""
    return render_template('dashboard.html')
    
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    """This method authenticates a user based on his/her user/login credentials"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            """Generating a token for the session"""
            token = "user-token"
            login_user(user)
            return redirect(url_for('auth.dashboard'))
        else:
            return jsonify({"message":"Invalid user credentials. Please try again"}), 401
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """This method discards/invalidates the session token created in 'login' method and logs out the user"""
    logout_user()
    return jsonify({"message":"User is logged out successfully."}), 200
