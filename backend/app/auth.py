from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db  # Ensure this is the correct import path for your models

auth_blueprint = Blueprint('auth', __name__)

# API
# Authorization and Authentication
@auth_blueprint.route('/register', methods=['POST'])
def register():
    print("THIS FUNCTION IS WORKING AHAHAH")
    # Get email and password from request
    email = request.json.get('email')
    password = request.json.get('password')
    print("SET THE PASSWORD AND EMAIL")
    # Validate the input
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400
    print("NO ERROR")

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    print("existing user blah blah blah")
    # Create new user with hashed password
    new_user = User(email=email)
    new_user.password_hash = generate_password_hash(password)
    db.session.add(new_user)
    db.session.commit()

    print("working next line is retuen!")
    # Respond back with success message
    return jsonify({'message': 'User registered successfully'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    # Get email and password from request
    email = request.json.get('email')
    password = request.json.get('password')

    # Validate the input
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    # Authenticate user
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        # Create JWT token
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Get the identity of the current user
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200