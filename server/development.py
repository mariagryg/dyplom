from dotenv import load_dotenv
import os
from flask import Flask

# Load environment variables from .env.local file
load_dotenv('../.env.local')  # Update the path if necessary

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'defaultsecretkey')

# Define routes
@app.route('/')
def home():
    return "Welcome to the Flask application!"

# Run the app with port 5555 and in debug mode
if __name__ == "__main__":
    app.run(port=5555, debug=True)
