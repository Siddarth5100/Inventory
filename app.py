from flask import Flask
from db import db
from models import create_tables

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Sid5100#!1@localhost/inventory"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 

@app.route("/")
def hello_world():
    return "<p>Hello Siddhu</p>"


if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(debug=True)