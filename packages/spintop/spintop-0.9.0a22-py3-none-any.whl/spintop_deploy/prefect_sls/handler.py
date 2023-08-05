from flask import Flask

def create_app(prefect_context):
    app = Flask(__name__)
    blueprint = prefect_context.flask_blueprint()
    app.register_blueprint(blueprint)
