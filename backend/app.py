
from flask import Flask

from config import Config

from routes.home import home_bp
from routes.users import users_bp
from routes.resume import resume_bp
from routes.job import job_bp
from routes.analysis import analysis_bp


# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# LOAD CONFIGURATION
# ============================================================

app.config.from_object(Config)


# ============================================================
# REGISTER BLUEPRINTS
# ============================================================

app.register_blueprint(home_bp)



app.register_blueprint(users_bp)

app.register_blueprint(resume_bp)

app.register_blueprint(job_bp)

app.register_blueprint(analysis_bp)


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=app.config["DEBUG"]
    )
