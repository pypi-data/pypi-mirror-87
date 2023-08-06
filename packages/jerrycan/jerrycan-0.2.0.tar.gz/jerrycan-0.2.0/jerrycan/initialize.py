"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of jerrycan.

jerrycan is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

jerrycan is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with jerrycan.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import sys
import base64
import binascii
import logging
import sentry_sdk
import traceback
from logging.handlers import TimedRotatingFileHandler
from sqlalchemy.exc import OperationalError
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from typing import List, Optional, Type, Callable, Tuple, Dict, Any
from flask import redirect, url_for, flash, render_template
from flask.logging import default_handler
from flask.blueprints import Blueprint
from werkzeug.exceptions import HTTPException
from jerrycan.Config import Config
from jerrycan.base import app, login_manager, db
from jerrycan.enums import AlertSeverity
from jerrycan.db.User import User
from jerrycan.db.ApiKey import ApiKey
from jerrycan.db.TelegramChatId import TelegramChatId
from jerrycan.routes import blueprint_generators \
    as default_blueprint_generators


CREATED_BLUEPRINTS = []
"""
Keeps track of created blueprint names.
This is necessary for unit testing with nose, because duplicate blueprint names
will cause errors.
"""


def init_flask(
        module_name: str,
        sentry_dsn: str,
        root_path: str,
        config: Type[Config],
        models: List[Type[db.Model]],
        blueprint_generators: List[Tuple[Callable[[str], Blueprint], str]],
        extra_jinja_vars: Optional[Dict[str, Any]] = None
):
    """
    Initializes the flask application
    :param module_name: The name of the module
    :param sentry_dsn: The sentry DSN used for error logging
    :param root_path: The root path of the flask application
    :param config: The Config class to use for configuration
    :param models: The database models to create
    :param blueprint_generators: Tuples that contain a function that generates
                                 a blueprint and the name of the blueprint
    :param extra_jinja_vars: Any extra variables to pass to jinja
    :return: None
    """
    app.root_path = root_path
    config.load_config(root_path, module_name, sentry_dsn)
    __init_logging(config)

    default_models = [
        User,
        ApiKey,
        TelegramChatId
    ]

    if extra_jinja_vars is None:
        extra_jinja_vars = {}
    __init_app(
        config,
        default_blueprint_generators + blueprint_generators,
        extra_jinja_vars
    )
    __init_db(config, default_models + models)
    __init_login_manager()


def __init_logging(config: Type[Config]):
    """
    Sets up logging to a logfile
    :param config: The configuration to use
    :return: None
    """
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=None
    )
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[FlaskIntegration(), sentry_logging]
    )

    app.logger.removeHandler(default_handler)

    log_format = \
        "[%(asctime)s, %(levelname)s] %(module)s[%(lineno)d]: %(message)s"
    formatter = logging.Formatter(log_format)

    info_handler = TimedRotatingFileHandler(
        config.LOGGING_PATH,
        when="midnight",
        interval=1,
        backupCount=7
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    debug_handler = TimedRotatingFileHandler(
        config.DEBUG_LOGGING_PATH,
        when="midnight",
        interval=1,
        backupCount=7
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(config.VERBOSITY)
    stream_handler.setFormatter(formatter)

    app.logger.addHandler(info_handler)
    app.logger.addHandler(debug_handler)
    app.logger.addHandler(stream_handler)

    app.logger.setLevel(logging.DEBUG)


def __init_app(
        config: Type[Config],
        blueprint_generators: List[Tuple[Callable[[str], Blueprint], str]],
        extra_jinja_vars: Dict[str, Any]
):
    """
    Initializes the flask app
    :param config: The configuration to use
    :param blueprint_generators: Tuples that contain a function that generates
                                 a blueprint and the name of the blueprint
    :param extra_jinja_vars: Any extra variables to pass to jinja
    :return: None
    """
    app.testing = config.TESTING
    app.config["TRAP_HTTP_EXCEPTIONS"] = True
    app.config["SERVER_NAME"] = Config.base_url().split("://", 1)[1]
    app.secret_key = config.FLASK_SECRET
    for blueprint_generator, blueprint_name in blueprint_generators:
        if blueprint_name in CREATED_BLUEPRINTS:
            app.logger.debug(f"Blueprint {blueprint_name} already created")
            continue
        else:
            app.logger.info(f"Creating blueprint {blueprint_name}")
            CREATED_BLUEPRINTS.append(blueprint_name)
            blueprint = blueprint_generator(blueprint_name)
            app.register_blueprint(blueprint)

    @app.context_processor
    def inject_template_variables():
        """
        Injects the project's version string so that it will be available
        in templates
        :return: The dictionary to inject
        """
        defaults = {
            "version": config.VERSION,
            "env": app.env,
            "config": config
        }
        defaults.update(extra_jinja_vars)
        return defaults

    @app.errorhandler(Exception)
    def exception_handling(e: Exception):
        """
        Handles any uncaught exceptions and shows an applicable error page
        :param e: The caught exception
        :return: The response to the exception
        """
        if isinstance(e, HTTPException):
            error = e
            if e.code == 401:
                flash(
                    config.STRINGS["401_message"],
                    AlertSeverity.DANGER.value
                )
                return redirect(url_for("user_management.login"))
            app.logger.warning("Caught HTTP exception: {}".format(e))
        else:
            error = HTTPException(config.STRINGS["500_message"])
            error.code = 500
            trace = "".join(traceback.format_exception(*sys.exc_info()))
            app.logger.error("Caught exception: {}\n{}".format(e, trace))
            sentry_sdk.capture_exception(e)
        return render_template(
            config.REQUIRED_TEMPLATES["error_page"],
            error=error
        )

    @app.errorhandler(HTTPException)
    def unauthorized_handling(e: HTTPException):
        """
        Forwards HTTP exceptions to the error handler
        :param e: The HTTPException
        :return: The response to the exception
        """
        return exception_handling(e)


def __init_db(config: Type[Config], models: List[db.Model]):
    """
    Initializes the database
    :param config: The configuration to use
    :param models: The models to create in the database
    :return: None
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Makes sure that we don't get errors because
    # of an idle database connection
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    db.init_app(app)

    for model in models:
        app.logger.debug(f"Loading model {model.__name__}")

    with app.app_context():
        try:
            db.create_all()
        except OperationalError:
            print("Failed to connect to the database")
            sys.exit(1)


def __init_login_manager():
    """
    Initializes the login manager
    :return: None
    """
    login_manager.session_protection = "strong"

    # Set up login manager
    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        """
        Loads a user from an ID
        :param user_id: The ID
        :return: The User
        """
        return User.query.get(int(user_id))

    @login_manager.request_loader
    def load_user_from_request(request) -> Optional[User]:
        """
        Loads a user pased on a provided API key
        :param request: The request containing the API key in the headers
        :return: The user or None if no valid API key was provided
        """
        if "Authorization" not in request.headers:
            return None

        api_key = request.headers["Authorization"].replace("Basic ", "", 1)

        try:
            api_key = base64.b64decode(
                api_key.encode("utf-8")
            ).decode("utf-8")
        except (TypeError, binascii.Error):
            return None

        db_api_key = ApiKey.query.get(api_key.split(":", 1)[0])

        # Check for validity of API key
        if db_api_key is None or not db_api_key.verify_key(api_key):
            return None

        elif db_api_key.has_expired():
            db.session.delete(db_api_key)
            db.session.commit()
            return None

        return User.query.get(db_api_key.user_id)
