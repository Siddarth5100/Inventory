from db import db

class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.String(20), primary_key = True)
    product_name = db.Column(db.String(20), nullable = False)

class Location(db.Model):
    __tablename__ = "location"
    location_id = db.Column(db.String(20), primary_key = True)
    location_name = db.Column(db.String(20), nullable = False)

class Stock(db.Model):
    __tablename__ = "stock"
    product_id = db.Column(db.String(20), db.ForeignKey('product.product_id'), primary_key = True)
    location_id = db.Column(db.String(20), db.ForeignKey('location.location_id'), primary_key = True)
    qty = db.Column(db.Integer, default = 0)

class ProductMovement(db.Model):
    __tablename__ = "productmovement"
    movement_id = db.Column(db.String(20), primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False , )
    from_location = db.Column(db.String(20))
    to_location = db.Column(db.String(20))
    product_id = db.Column(db.String(20), db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer, nullable = False)


def create_tables():
    db.create_all()
    print("All tables created successfully")