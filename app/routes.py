from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from datetime import datetime
from .models import db, User, Prediction, TournamentActual
from .user_management import authenticate_user, get_all_usernames, update_user_pin
from .prediction_management import get_user_predictions, save_prediction, is_deadline_passed, get_all_teams
from .constants import GROUPS, RIVALRIES, GOLDEN_BOOT_PLAYERS, RIVALRY_TEAMS, DEADLINE, TOURNAMENT_END
from .scoring import calculate_total_score

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
    tournament_ended = datetime.utcnow() > TOURNAMENT_END
    return {'deadline_passed': is_deadline_passed(), 'deadline': DEADLINE, 'tournament_ended': tournament_ended}

@bp.route('/')
def index():
    return render_template('index.html', current_user=request.user)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        auth_result = authenticate_user(username, pin)
        
        if auth_result["success"]:
            user = auth_result["user"]
            session.clear()
            session['user_id'] = user.id
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash(auth_result["message"], 'error')
            
    usernames = get_all_usernames()
    return render_template('login.html', usernames=usernames, current_user=request.user)

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/change_pin', methods=['GET', 'POST'])
def change_pin():
    if not request.user:
        flash('Please login to change your PIN.', 'error')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        current_pin = request.form.get('current_pin')
        new_pin = request.form.get('new_pin')
        confirm_pin = request.form.get('confirm_pin')

        auth_result = authenticate_user(request.user.username, current_pin)
        if not auth_result["success"]:
            flash(auth_result["message"], 'error')
            return redirect(url_for('main.change_pin'))

        if new_pin != confirm_pin:
            flash('New PIN and Confirm New PIN do not match.', 'error')
            return redirect(url_for('main.change_pin'))

        if len(new_pin) != 4 or not new_pin.isdigit():
            flash('New PIN must be exactly 4 digits.', 'error')
            return redirect(url_for('main.change_pin'))

        if update_user_pin(request.user.id, new_pin):
            flash('Your PIN has been updated successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('An error occurred while updating your PIN.', 'error')
            return redirect(url_for('main.change_pin'))

    return render_template('change_pin.html', current_user=request.user)

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
            # Filter out empty values and check for duplicates
            filled_data = [d for d in data if d]
            if len(filled_data) != len(set(filled_data)):
                flash('Duplicate players selected in Golden Boot ranking. Please select unique players.', 'error')
                return redirect(url_for('main.predictions'))
        elif category == 'cat6':
            p32 = request.form.get('penalties_round_32')
            prest = request.form.get('penalties_knockout_rest')
            
            try:
                if p32 and not (0 <= int(p32) <= 16):
                    raise ValueError
                if prest and not (0 <= int(prest) <= 16):
                    raise ValueError
            except (ValueError, TypeError):
                flash('Shoot-out numbers must be between 0 and 16.', 'error')
                return redirect(url_for('main.predictions'))

            data = {
                'winner': request.form.get('winner'),
                'runner_up': request.form.get('runner_up'),
                'third_place': request.form.get('third_place'),
                'penalties_round_32': p32,
                'penalties_knockout_rest': prest,
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
    for cat in ['cat1', 'cat2', 'cat4', 'cat6']:
        if cat not in user_preds:
            user_preds[cat] = {}
    for cat in ['cat3', 'cat5']:
        if cat not in user_preds:
            user_preds[cat] = []
            
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
    users = User.query.all()
    actuals = TournamentActual.query.all()
    tournament_actuals = {a.category: a.actual_data for a in actuals}

    scoreboard_data = []
    for user in users:
        user_preds = get_user_predictions(user.id)
        scores = calculate_total_score(user_preds, tournament_actuals)
        scoreboard_data.append({
            'username': user.username,
            'scores': scores
        })

    # Sort descending by total score
    scoreboard_data.sort(key=lambda x: x['scores']['total'], reverse=True)

    if request.headers.get('HX-Request'):
        return render_template('partials/scoreboard_table.html', scoreboard_data=scoreboard_data)

    return render_template('scoreboard.html', current_user=request.user, scoreboard_data=scoreboard_data)

@bp.route('/admin/actuals', methods=['GET', 'POST'])
def admin_actuals():
    if not request.user or not request.user.is_admin:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        category = request.form.get('category')
        
        # Similar data gathering logic to predictions
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
            p32 = request.form.get('penalties_round_32')
            prest = request.form.get('penalties_knockout_rest')
            data = {
                'winner': request.form.get('winner'),
                'runner_up': request.form.get('runner_up'),
                'third_place': request.form.get('third_place'),
                'penalties_round_32': p32,
                'penalties_knockout_rest': prest,
                'host_success': request.form.get('host_success'),
                'wipeout_exists': request.form.get('wipeout_exists')
            }
        else:
            flash('Invalid category.', 'error')
            return redirect(url_for('main.admin_actuals'))

        actual = TournamentActual.query.filter_by(category=category).first()
        if actual:
            actual.actual_data = data
        else:
            actual = TournamentActual(category=category, actual_data=data)
            db.session.add(actual)
        
        db.session.commit()
        flash(f'Actuals for Category {category[3:]} saved successfully!', 'success')
        return redirect(url_for('main.admin_actuals'))

    actuals_db = TournamentActual.query.all()
    tournament_actuals = {a.category: a.actual_data for a in actuals_db}

    # Ensure all categories exist in dict
    for cat in ['cat1', 'cat2', 'cat4', 'cat6']:
        if cat not in tournament_actuals:
            tournament_actuals[cat] = {}
    for cat in ['cat3', 'cat5']:
        if cat not in tournament_actuals:
            tournament_actuals[cat] = []

    all_teams = get_all_teams()

    return render_template('admin_actuals.html',
                           current_user=request.user,
                           actuals=tournament_actuals,
                           groups=GROUPS,
                           rivalries=RIVALRIES,
                           rivalry_teams=RIVALRY_TEAMS,
                           players=GOLDEN_BOOT_PLAYERS,
                           all_teams=all_teams)

@bp.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    if not request.user or not request.user.is_admin:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        if user:
            user.failed_login_attempts = 0
            user.is_locked = False
            db.session.commit()
            flash(f'Account for {user.username} has been unlocked.', 'success')
        return redirect(url_for('main.admin_users'))

    all_users = User.query.order_by(User.username).all()
    return render_template('admin_users.html', current_user=request.user, users=all_users)
