# (C) Copyright IBM Corp. 2020.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from configparser import ConfigParser
import logging

class LogConfig:
    specific_log_level = logging.WARN
    filename = None

def get_logger(name, specific_log_level=None):
    default_log_level = LogConfig.specific_log_level

    config = ConfigParser()
    config.read("./config.ini")

    try:
        filename = config.get("DEFAULT", 'log-filename')
    except:
        filename = LogConfig.filename

    log_level = default_log_level

    try:
        env_log_level = getattr(logging, config.get("DEFAULT", 'log'), None)
    except:
        env_log_level = None

    if env_log_level is not None:
        log_level = env_log_level

    if specific_log_level is not None:
        log_level = specific_log_level

    if not isinstance(log_level, int):
        raise ValueError('Invalid log level: %s' % log_level)

    logger = logging.getLogger(name)
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", filename=filename)
    logger.setLevel(log_level)
    return logger
