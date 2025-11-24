from flask import Flask
from db import db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Sid5100#!1@localhost/inventory"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 

@app.route("/")
def hello_world():
    return "<p>Hello Siddhu</p>"


if __name__ == "__main__":
    app.run(debug=True)