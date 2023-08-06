#!/usr/bin/env python3
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

import fire
from sys import exit, stdin, stdout
from typing import Optional
from .configuration import DEFAULT_ENCODING
from .flattener import Flattener
from .logging import setup_logger


def _run(
    jsonplan: Optional[str] = "",
    output: Optional[str] = "",
    debug: Optional[bool] = False,
) -> None:
    """
    Starts the execution of the Flatplan application.

    Parameters
    ----------
    jsonplan : str, optional
        a path pointing to the location of the terraform plan in JSON format, default it reads from stdin

    output : str, optional
        a file path where we will save the flattened plan file in JSON format, default it writes to stdout

    debug : bool, optional
        whether we show debug log messages or not, default: false

    Returns
    -------
    None.
    """

    logger = setup_logger("flatplan", debug)
    fp_in = stdin
    fp_out = stdout

    logger.debug("Flattening...")

    if jsonplan:
        logger.debug(f"Reading plan from {jsonplan}")
        fp_in = open(jsonplan, "r", encoding=DEFAULT_ENCODING)

    if output:
        logger.debug(f"Output will be saved to {output}")
        fp_out = open(output, "w+", encoding=DEFAULT_ENCODING)

    json_in = fp_in.read()
    flattener = Flattener(json_in, logger=logger)
    json_out = flattener.flatten()
    fp_out.write(f"{json_out}\n")
    fp_in.close()
    fp_out.close()

    logger.debug("Flattened!")


def main() -> None:
    """
    A wrapper for the _run function also providing CLI parameter parsing.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """
    fire.Fire(_run)
    exit(0)


if __name__ == "__main__":
    main()
