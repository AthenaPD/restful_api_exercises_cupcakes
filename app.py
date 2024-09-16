"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from models import db, Cupcake, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home_page():
    """Renders html template that includes some JS"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

# *****************************
# RESTFUL CUPCAKES JSON API
# *****************************
@app.route('/api/cupcakes')
def list_all_cupcakes():
    """
    View function to show all cupcakes.
    Return JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]}
    """

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """Return JSON {'cupcake': {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """
    Create cupcake from form data & return it.
    Returns JSON {'cupcake': {id, flavor, size, rating, image}}
    """
    
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image', None)

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcake/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """
    return JSON {'cupcake': {id, flavor, size, rating, image}}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcake/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """
    Delete a cupcake and return JSON {'message': 'deleted'}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='deleted')


