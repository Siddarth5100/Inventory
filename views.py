from db import db
from models import Product, Location, Stock, ProductMovement
from flask import request, jsonify, render_template, Blueprint

api = Blueprint('api', __name__)

# functions



# API's

# for adding new product in db
@api.route('/add_new_product', methods = ['POST'])   
def add_new_product():
    user_input = request.get_json()

    # product name already exist validation
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
    
    # locationname already exist validation
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

    # if both location empty validation
    if data["from_location"] is None and data["to_location"] is None:
        return jsonify({
            "message": "Either from_location or to_location must be provided"
        })
    
    # from location empty validation
    if data["from_location"] is not None:
        if not Location.query.filter_by(location_id = data["from_location"]).first():
            return jsonify({
                "message": "From location doesn't exist"
            })
        
    # to location empty validation
    if data["to_location"] is not None:
        if not Location.query.filter_by(location_id = data["to_location"]).first():
            return jsonify({
                "message": "To location doesn't exist"
            })

    # product empty validation
    if not Product.query.filter_by(product_id = data["product_id"]).first():
        return jsonify({
            "message" : "Product does not exist"
        })


    # check quantity in stock table
    from_loc = Location.query.filter_by(location_name = data["from_location"]).first()
    
    if not from_loc:
        return jsonify({
            "message": "Location does not exist"
        })
    
    from_loc_id = from_loc.location_id

    product = Stock.query.filter_by(location_id = from_loc_id, product_id = data["product_id"]).first()
        
    if not product:
        return jsonify({
            "message": "Location doesn't have the product"
        })
    
    if product.qty < data["qty"]:
        return jsonify({
            "message": "Not enough stock"
        })

    to_loc = Location.query.filter_by(location_name = data["to_location"]).first()
    to_loc_id = to_loc.location_id


    # adding in db
    try:
        new_product_movement = ProductMovement(
            from_location = from_loc_id,
            to_location = to_loc_id,
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

    # data validation
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

    # data validation
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


# fetching the product details
@api.route('/get_products', methods = ['GET'])
def get_products():
    products = Product.query.all()

    product_list = []
    for product in products:
        product_list.append({
            "product_id": product.product_id,
            "product_name": product.product_name
        })

    return jsonify(product_list)

# rendering products available
@api.route('/products_available', methods = ['GET'])
def products_available():
    return render_template('products.html')


# feching the location details
@api.route('/get_locations', methods = ['GET'])
def get_locations():
    locations = Location.query.all()

    location_list = []
    for location in locations:
        location_list.append({
            "location_id": location.location_id,
            "location_name": location.location_name
        })

    return jsonify(location_list)

# rendering locations available
@api.route('/locations_available', methods = ['GET'])
def locations_available():
    return render_template('locations.html')


# fetching productmovements details
@api.route('/get_productmovements', methods = ['GET'])
def get_productmovements():
    productmovements = ProductMovement.query.all()

    productmovement_list = []
    for productmovement in productmovements:
        productmovement_list.append({
            "movement_id": productmovement.movement_id,
            "time_stamp": productmovement.time_stamp,
            "from_location": productmovement.from_location,
            "to_location": productmovement.to_location,
            "product_id": productmovement.product_id,
            "qty": productmovement.qty
        })
        

    return jsonify(productmovement_list)

# rendering the productmovements_available
@api.route('/productmovements_available', methods = ['GET'])
def productmovements_available():
    return render_template('productmovements.html')


# delete product
@api.route('/delete_product', methods = ['DELETE'])
def delete_product():
    data = request.get_json()

    product = Product.query.filter_by(product_id = data["product_id"]).first()

    # product validation
    if not product:
        return jsonify({
            "message": "Product not found"
        })

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully"
    })


# delete location
@api.route('/delete_location', methods = ['DELETE'])
def delete_locations():
    data = request.get_json()

    location = Location.query.filter_by(location_id = data["location_id"]).first()

    # location validation
    if not location:
        return jsonify({
            "message": "Location not found"
        })
    
    db.session.delete(location)
    db.session.commit()

    return jsonify({
        "message": "Location deleted successfully"
    })
