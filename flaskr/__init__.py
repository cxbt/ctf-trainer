import os
from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import chall
    app.register_blueprint(chall.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import scoreboard
    app.register_blueprint(scoreboard.bp)

    app.add_url_rule('/', endpoint='index')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
