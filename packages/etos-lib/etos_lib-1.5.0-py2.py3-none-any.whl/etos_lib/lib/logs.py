# Copyright 2020 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""ETOS Library log handler."""
import os
import logging
from pydantic import BaseModel  # pylint:disable=no-name-in-module
from .database import Database
from .config import Config


class Record(BaseModel):  # pylint:disable=too-few-public-methods
    """Log record model."""

    message: str
    level: int
    timestamp: int
    milliseconds: int


class EtosLogHandler(logging.StreamHandler):
    """Log handler for ETOS. Take all logs and write them to a database.

    Create loghandler by adding it to logging basicConfig:

        LOGFORMAT = "[%(asctime)s] %(levelname)s [%(name)s]: %(message)s"
        logging.basicConfig(level=logging.INFO, handlers=[EtosLogHandler()],
                            format=LOGFORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    """

    def __init__(self, *args, **kwargs):
        """Initialize database and config."""
        super().__init__(*args, **kwargs)
        self.database = Database()
        self.config = Config()

    def handle(self, record):
        """Log handler for sending record to database.

        :param record: Record to handle.
        :type record: :obj:`logging.LogRecord`
        """
        super().handle(record)
        message = {
            "message": record.message,
            "timestamp": record.created,
            "milliseconds": record.msecs,
            "level": record.levelno,
        }
        self.send(Record(**message))

    def send(self, record):
        """Send a record to database.

        :param record: Record to send.
        :type record: :obj:`Record`
        """
        if os.getenv("HOSTNAME") is not None:
            key = "{}:{}".format(self.config.get("service_name"), os.getenv("HOSTNAME"))
        else:
            key = self.config.get("service_name")

        self.database.append(
            key,
            {
                "{timestamp}.{milliseconds}:{level}:{message}".format(
                    **record.dict()
                ): record.timestamp
            },
        )
