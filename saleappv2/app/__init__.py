import cloudinary
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '18sdjksdgjs&%^&^(*@@*#&@#^@DGGHJHG'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledbv2?charset=utf8mb4" % quote('Admin"123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app=app)
login = LoginManager(app=app)

cloudinary.config(
    cloud_name="duc03aacd",
    api_key="172198183281785",
    api_secret="n75A1ZuGe_h3AQ5o3ulhfIBk9KU"
)


