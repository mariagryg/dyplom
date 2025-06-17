from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import MetaData
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure app settings from environment variables
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Secret key for sessions and security
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')  # Database URI from environment
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
app.json.compact = False  # Pretty print JSON responses

# JWT configurations
app.config["JWT_COOKIE_SECURE"] = True  # Set to True for secure cookies in production
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Secret key for JWT
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Store JWT in cookies
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Expiry time for JWT access tokens

# Initialize the extensions
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Set up SQLAlchemy
db = SQLAlchemy(metadata=metadata)
db.init_app(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Set up Flask-Restful for building REST APIs
api = Api(app)

# Initialize Flask-Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-JWT-Extended for handling JSON Web Tokens
jwt = JWTManager(app)

# Enable Cross-Origin Resource Sharing (CORS) to allow frontend communication with this backend
CORS(app, supports_credentials=True)

# Application entry point for testing purposes
@app.route('/')
def index():
    return jsonify(message="Welcome to the API!")

# Sample route for testing authentication (secured with JWT)
@app.route('/protected', methods=["GET"])
@jwt_required()
def protected():
    return jsonify(message="This is a protected route"), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)  # Running in debug mode during development
