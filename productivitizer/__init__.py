import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # SECRET_KEY must be overriden when deploying
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "productivitizer.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Importing the init app function from db.py
    """
    After importing we can call the init-db command,
    $ flask --app productivitizer init-db

    """
    # Importing database blueprint
    from . import db

    db.init_app(app)

    # Importing homepage blueprint
    from . import homepage

    app.register_blueprint(homepage.bp)
    app.add_url_rule("/", endpoint="index")

    # Importing auth blueprint
    from . import auth

    app.register_blueprint(auth.bp)

    # Importing pomodoro blueprint
    from . import pomodoro

    app.register_blueprint(pomodoro.bp)

    # Import kanban blueprint
    from . import kanban

    app.register_blueprint(kanban.bp)

    # Import finance blueprint
    from . import finance

    app.register_blueprint(finance.bp)

    return app
