from flask import Flask
from config import Config
from routes.home import home_bp
from routes.users import users_bp
from routes.resume import resume_bp

app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(resume_bp)

app.register_blueprint(home_bp)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])