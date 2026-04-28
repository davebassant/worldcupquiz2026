from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from .models import db, User, Prediction
from .user_management import authenticate_user, get_all_usernames
from .prediction_management import get_user_predictions, save_prediction, is_deadline_passed, get_all_teams
from .constants import GROUPS, RIVALRIES, GOLDEN_BOOT_PLAYERS, RIVALRY_TEAMS, DEADLINE

bp = Blueprint('main', __name__)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        request.user = None
    else:
        request.user = User.query.get(user_id)

@bp.app_context_processor
def inject_deadline():
    return {'deadline_passed': is_deadline_passed(), 'deadline': DEADLINE}

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

@bp.route('/predictions', methods=['GET', 'POST'])
def predictions():
    if not request.user:
        flash('Please login to view predictions.', 'error')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        if is_deadline_passed():
            flash('Deadline has passed. Predictions can no longer be edited.', 'error')
            return redirect(url_for('main.predictions'))
            
        category = request.form.get('category')
        
        # Handle different categories
        if category == 'cat1':
            data = {
                'most_goals_scored': request.form.get('most_goals_scored'),
                'fewest_goals_scored': request.form.get('fewest_goals_scored'),
                'most_goals_conceded': request.form.get('most_goals_conceded'),
                'fewest_goals_conceded': request.form.get('fewest_goals_conceded')
            }
        elif category == 'cat2':
            data = {}
            for group in GROUPS.keys():
                data[group] = [request.form.get(f'{group}_1'), request.form.get(f'{group}_2')]
        elif category == 'cat3':
            data = request.form.getlist('lucky_8')
        elif category == 'cat4':
            data = {rivalry[0]: request.form.get(rivalry[0]) for rivalry in RIVALRIES}
        elif category == 'cat5':
            data = [request.form.get(f'player_{i}') for i in range(1, 6)]
        elif category == 'cat6':
            data = {
                'winner': request.form.get('winner'),
                'runner_up': request.form.get('runner_up'),
                'third_place': request.form.get('third_place'),
                'penalty_shootouts': request.form.get('penalty_shootouts'),
                'host_success': request.form.get('host_success'),
                'wipeout_exists': request.form.get('wipeout_exists')
            }
        else:
            flash('Invalid category.', 'error')
            return redirect(url_for('main.predictions'))

        success, message = save_prediction(request.user.id, category, data)
        if success:
            flash(f'Category {category[3:]} saved successfully!', 'success')
        else:
            flash(message, 'error')
        
        return redirect(url_for('main.predictions'))

    user_preds = get_user_predictions(request.user.id)
    # Ensure all categories exist in the dict to prevent template errors
    for cat in ['cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6']:
        if cat not in user_preds:
            user_preds[cat] = {}
            
    all_teams = get_all_teams()
    
    return render_template('predictions.html', 
                           current_user=request.user, 
                           predictions=user_preds,
                           groups=GROUPS,
                           rivalries=RIVALRIES,
                           rivalry_teams=RIVALRY_TEAMS,
                           players=GOLDEN_BOOT_PLAYERS,
                           all_teams=all_teams)

@bp.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard.html', current_user=request.user)
