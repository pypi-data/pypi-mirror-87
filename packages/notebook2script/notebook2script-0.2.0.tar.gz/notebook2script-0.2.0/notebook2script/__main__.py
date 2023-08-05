#!/usr/bin/env python3
#
#  __main__.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 2
#  as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import sys
from typing import Tuple

# 3rd party
import click
from consolekit import click_command

__all__ = ["main"]


@click.argument("notebooks", metavar="NOTEBOOK", type=click.STRING, nargs=-1)
@click.option("-o", "--outdir", type=click.STRING, default='.', help="Directory to save the output scripts in.")
@click.option("-f", "--overwrite", is_flag=True, default=False, help="Overwrite existing files.")
@click_command()
def main(notebooks: Tuple[str, ...], outdir: str = '.', overwrite: bool = False):
	"""
	Convert Jupyter Notebooks to Python scripts.
	"""

	# stdlib
	import glob
	from itertools import chain

	# this package
	from notebook2script import process_multiple_notebooks

	notebooks = tuple(chain.from_iterable(glob.glob(notebook) for notebook in notebooks))

	# print(notebooks)
	# print(notebooks[0])

	if not notebooks:
		sys.exit(0)
	else:
		sys.exit(process_multiple_notebooks(notebooks, outdir, overwrite=overwrite))


if __name__ == "__main__":
	try:
		sys.exit(main())
	except KeyboardInterrupt:
		sys.exit(1)
