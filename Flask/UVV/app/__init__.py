from flask import Flask

def create_app(config_name = 'development'):
    app = Flask(__name__)

    if config_name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    elif config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DefaultConfig')

    app.debug = app.config.get('DEBUG', False)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app