from flask import Flask
import os
from dotenv import load_dotenv
from views import app_bp


load_dotenv()


def create_app():
    app = Flask("JokesAPI")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(app_bp)
    return app


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app = create_app()
    app.debug = True
    app.run(host='0.0.0.0', port=port)
