from db import db

class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(255), nullable = False)

class Location(db.Model):
    __tablename__ = "location"
    location_id = db.Column(db.Integer, primary_key = True)
    location_name = db.Column(db.String(255), nullable =False)

class ProductMovement(db.Model):
    __tablename__ = "productmovement"
    movement_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    timestamp = db.Column(db.DateTime, nullable = False)
    from_location = db.Column(db.Integer)
    to_location = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer, nullable = False)