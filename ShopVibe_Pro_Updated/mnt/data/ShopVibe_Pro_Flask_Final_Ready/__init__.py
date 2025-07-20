
import os
import json
from flask import Flask, session, request, g
from dotenv import load_dotenv
from pymongo import MongoClient
import stripe

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client.get_default_database()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # MongoDB
    app.mongo = mongo_db

    # Stripe
    app.stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY")
    app.stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    # i18n settings
    app.default_language = os.getenv("DEFAULT_LANGUAGE", "en")
    app.supported_languages = os.getenv("SUPPORTED_LANGUAGES", "en").split(",")

    @app.before_request
    def load_language():
        lang = request.args.get("lang") or session.get("lang") or app.default_language
        if lang not in app.supported_languages:
            lang = app.default_language
        session["lang"] = lang
        lang_file = os.path.join(app.root_path, "data", "lang", f"{lang}.json")
        try:
            with open(lang_file, encoding="utf-8") as f:
                g.t = json.load(f)
        except:
            g.t = {}

    @app.context_processor
    def inject_translations():
        return {"t": g.get("t", {})}

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
