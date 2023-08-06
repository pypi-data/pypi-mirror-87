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
import time
import logging
import sentry_sdk
import traceback
from threading import Thread
# noinspection PyPackageRequirements
from telegram.error import TimedOut
from typing import Callable, Tuple, Dict, Type
from cheroot.wsgi import Server, PathInfoDispatcher
from jerrycan.background.telegram import telegram_whoami
from jerrycan.base import app
from jerrycan.Config import Config


def __start_background_tasks(
        task_definitions: Dict[str, Tuple[int, Callable]]
):
    """
    Starts background tasks for a flask application
    :param task_definitions: The background tasks, consisting of:
                                - the name of the task
                                - the time to wait before running
                                  the task again
                                - a function that takes no arguments that
                                  executes the task
    :return: None
    """
    def task_factory(_name: str, _delay: int, _function: Callable) -> Thread:
        def run_task():
            while True:
                try:
                    with app.app_context():
                        _function()
                except Exception as error:
                    app.logger.error(f"Encountered exception in "
                                     f"background task {_name}: {error}\n"
                                     f"{traceback.format_exc()}")
                    sentry_sdk.capture_exception(error)
                time.sleep(_delay)
        return Thread(target=run_task)

    tasks = []
    for name, (delay, function) in task_definitions.items():
        tasks.append(task_factory(name, delay, function))

    for thread in tasks:
        thread.start()


def start_server(
        config: Type[Config],
        task_definitions: Dict[str, Tuple[int, Callable]]
):
    """
    Starts the flask application using a cheroot WSGI server
    :param config: The configuration to use
    :param task_definitions: The background tasks, consisting of:
                                - the name of the task
                                - the time to wait before running
                                  the task again
                                - a function that takes no arguments that
                                  executes the task
    :return: None
    """
    if not config.TELEGRAM_API_KEY == "" \
            and not config.TESTING \
            and config.TELEGRAM_WHOAMI:  # pragma: no cover
        try:
            config.initialize_telegram()
            Config.TELEGRAM_BOT_CONNECTION.bot.logger.setLevel(logging.WARNING)
        except TimedOut:
            print("Could not initialize telegram")
            sys.exit(1)
        task_definitions.update({
            "telegram_bg": (30, telegram_whoami)
        })
    __start_background_tasks(task_definitions)

    app.logger.info("STARTING FLASK")
    server = Server(
        ("0.0.0.0", config.HTTP_PORT),
        PathInfoDispatcher({"/": app})
    )

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
