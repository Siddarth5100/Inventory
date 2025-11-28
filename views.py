from db import db
from models import Product, Location, Stock, ProductMovement
from flask import request, jsonify, render_template, Blueprint

api = Blueprint('api', __name__)

# API's


# for adding new product in db
@api.route('/add_new_product', methods = ['POST'])   
def add_new_product():
    user_input = request.get_json()

    if Product.query.filter_by(product_name=user_input["product_name"]).first():
        return jsonify({
            "status" : "product name already exist"
        })
        
    try:
        new_product = Product(product_name = user_input["product_name"])
        
        db.session.add(new_product)    
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error"})

    return jsonify({
        "status": "added successfully",
        "product_id": new_product.product_id,
        "product_name": new_product.product_name
    })


# for adding new location(ware_house) in db
@api.route('/add_new_location', methods = ['POST'])
def add_new_location():
    user_input = request.get_json()
    
    if Location.query.filter_by(location_name = user_input["location_name"]).first():
        return jsonify({
            "status" : "location name already exist"
        })
    
    try:
        new_location = Location(location_name = user_input["location_name"])

        db.session.add(new_location)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error"})

    return jsonify({
          "status": "successfully added",
          "location_id": new_location.location_id,
          "location_name": new_location.location_name
    })


# adding product_movement
@api.route('/add_product_movement', methods = ['POST'])
def add_product_movement():
    data = request.get_json()

    # both location check
    if data["from_location"] is None and data["to_location"] is None:
        return jsonify({
            "message": "Either from_location or to_location must be provided"
        })
    
    # from location
    if data["from_location"] is not None:
        if not Location.query.filter_by(location_id = data["from_location"]).first():
            return jsonify({
                "message": "From location doesn't exist"
            })
        
    # to location
    if data["to_location"] is not None:
        if not Location.query.filter_by(location_id = data["to_location"]).first():
            return jsonify({
                "message": "To location doesn't exist"
            })

    # product
    if not Product.query.filter_by(product_id = data["product_id"]).first():
        return jsonify({
            "message" : "Product does not exist"
        })

    # check quantity in stock table
    


    # adding in db
    try:
        new_product_movement = ProductMovement(
            from_location = data["from_location"],
            to_location = data["to_location"],
            product_id = data["product_id"],
            qty = data["qty"]
        )

        db.session.add(new_product_movement)
        # db.session.commit()


    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error"
        })
    
    return jsonify({
        "status": "success",
        "from_location": new_product_movement.from_location,
        "to_location": new_product_movement.to_location,
        "product_id": new_product_movement.product_id,
        "qty": new_product_movement.qty
    })
    

# edit product name
@api.route('/product_name_edit', methods = ['PATCH'])
def product_name_edit():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "data not found"
        })

    product = Product.query.filter_by(product_id = data["product_id"]).first()  
    product.product_name = data["product_name"]

    # db.session.commit()

    return jsonify({
        "message": "product_name successfully updated",
        "updated_name": product.product_name
    })


# edit location name
@api.route('/location_name_edit', methods = ['PATCH'])
def location_name_edit():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "data not found"
        })
    
    location = Location.query.filter_by(location_id = data["location_id"]).first()
    location.location_name = data["location_name"]

    # db.session.commit()

    return jsonify({
        "message" : "location_name successfully updated",
        "location_name" : location.location_name
    })

