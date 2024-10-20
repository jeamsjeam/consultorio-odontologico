from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# create the application instance
app = Flask(__name__)

#postgresql://postgres:admin@localhost:5432/ipasme
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost:3306/ipasprueba"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create the application database instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import rol
from .routes import rolesController