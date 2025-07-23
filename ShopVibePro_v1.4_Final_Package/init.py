import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import stripe

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")
    mongo_uri = os.getenv("MONGO_URI")
    mongo_client = MongoClient(mongo_uri)
    app.mongo = mongo_client["shopvibe"]
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
