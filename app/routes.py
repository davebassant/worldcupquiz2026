from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import db, User, Prediction
from .user_management import authenticate_user, get_all_usernames

bp = Blueprint('main', __name__)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        request.user = None
    else:
        request.user = User.query.get(user_id)

@bp.route('/')
def index():
    return render_template('index.html', current_user=request.user)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        user = authenticate_user(username, pin)
        
        if user:
            session.clear()
            session['user_id'] = user.id
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid PIN. Please try again.', 'error')
            
    usernames = get_all_usernames()
    return render_template('login.html', usernames=usernames, current_user=request.user)

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/predictions')
def predictions():
    if not request.user:
        flash('Please login to view predictions.', 'error')
        return redirect(url_for('main.login'))
    return render_template('predictions.html', current_user=request.user)

@bp.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard.html', current_user=request.user)
