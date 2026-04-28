from app import create_app, db
from app.models import User
from app.user_management import init_users

app = create_app()

with app.app_context():
    db.create_all()
    init_users()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
