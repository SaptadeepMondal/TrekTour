from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from config import Config
from models import User
from routes import auth, admin, staff, user, api
from mongoengine import connect

app = Flask(__name__)
app.config.from_object(Config)
connect(host=app.config['MONGODB_SETTINGS']['host'])



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()



app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(staff)
app.register_blueprint(user)
app.register_blueprint(api)



with app.app_context():
    admin_user = User.objects(role="admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            name="Administrator",
            email="admin@trek.com",
            phone="9999999999",
            password=generate_password_hash("admin123"),
            role="admin",
            status="approved"
        )

        admin_user.save()
        print("Default Admin Created")


if __name__ == "__main__":
    app.run(debug=True, port=5000)