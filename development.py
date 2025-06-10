from dotenv import load_dotenv


load_dotenv('../.env.local')

from app import app
app.run(port=5555, debug=True)