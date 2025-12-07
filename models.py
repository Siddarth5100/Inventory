from db import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    product_name = db.Column(db.String(20), nullable = False)

class Location(db.Model):
    __tablename__ = "location"
    location_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    location_name = db.Column(db.String(20), nullable = False)

class Stock(db.Model):
    __tablename__ = "stock"
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key = True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), primary_key = True)
    qty = db.Column(db.Integer, default = 0)

class ProductMovement(db.Model):
    __tablename__ = "productmovement"
    movement_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer, nullable = False)

    from_location = db.relationship('Location', foreign_keys=[from_location_id])
    to_location = db.relationship('Location', foreign_keys=[to_location_id])
    product = db.relationship('Product')

def create_tables():
    db.create_all()
    print("All tables created successfully")