from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from config import Config
from models import User
from routes import auth, admin, staff, user, api
from mongoengine import connect

app = Flask(__name__)
app.config.from_object(Config)

# Safely connect to MongoDB
mongo_uri = app.config['MONGODB_SETTINGS']['host']
if mongo_uri:
    connect(host=mongo_uri)
else:
    print("WARNING: MONGODB_URI is not set. Database connection will fail.")



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



# Admin creation should be done via a script, not on every lambda cold start



if __name__ == "__main__":
    app.run(debug=True, port=5000)