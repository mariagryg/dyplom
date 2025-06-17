from flask import Flask
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

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()  # Load .env file

# Flask configurations
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # Makes JSON pretty printed
app.config["JWT_COOKIE_SECURE"] = True  # Ensure cookies are sent over HTTPS (in production)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Use env var for JWT secret
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Store JWT in cookies
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Set expiration time for JWT tokens

# Initialize extensions
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy
db = SQLAlchemy(metadata=metadata)
db.init_app(app)

# Initialize Migrate
migrate = Migrate(app, db)

# Initialize API
api = Api(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize JWT Manager for handling JSON Web Tokens
jwt = JWTManager(app)

# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app, supports_credentials=True)

# For debugging, you can print the database URI (ensure it doesn't expose sensitive data in production)
print("Database URI:", os.getenv('DATABASE_URI'))

# Application entry point (Optional: Useful if you want to start the app directly from this script)
if __name__ == "__main__":
    app.run(debug=True)
