# This file is part of Flatplan.
#
# Flatplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flatplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flatplan.  If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import Optional


def setup_logger(name: str, debug: Optional[bool] = False) -> logging.Logger:
    """
    Creates a logger object

    Parameters:
        name (str): The name of the logger, usually is the name of the application, class or method
        debug (bool): Whether we show debug log messages or not, default: false

    Returns:
         logger (logging.Logger): An object to be used to print out log messages
    """
    logger = logging.getLogger(name)
    level = "DEBUG" if debug else "INFO"

    try:
        import coloredlogs

        coloredlogs.install(level=level, logger=logger)
    except ImportError:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter("")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger
