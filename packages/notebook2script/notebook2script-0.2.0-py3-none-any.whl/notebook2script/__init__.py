#!/usr/bin/env python3
#
#  __init__.py
"""
Convert Jupyter Notebooks to Python Scripts.
"""
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
import os
import pathlib
from typing import Iterable, Union

# 3rd party
import isort  # type: ignore
import yapf_isort
from domdf_python_tools.compat import importlib_resources
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from nbconvert import PythonExporter  # type: ignore
from pre_commit_hooks.fix_encoding_pragma import fix_encoding_pragma  # type: ignore

# this package
from notebook2script.pointless import Pointless

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "GPLv2"
__version__: str = "0.2.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"process_multiple_notebooks",
		"convert_notebook",
		"reformat_file",
		]

linter = Pointless()
py_exporter = PythonExporter()


def convert_notebook(
		nb_file: PathLike,
		outfile: PathLike,
		):
	"""
	Convert a notebook to a Python file.

	:param nb_file: Filename of the Jupyter Notebook to convert.
	:param outfile: The filename to store the Python output as.
	"""

	nb_file = PathPlus(nb_file)
	outfile = PathPlus(outfile)
	outfile.parent.maybe_make()

	script, *_ = py_exporter.from_file(str(nb_file))

	outfile.write_clean(script)

	with importlib_resources.path("notebook2script", "isort.cfg") as isort_config:
		with importlib_resources.path("notebook2script", "style.yapf") as yapf_style:
			reformat_file(outfile, yapf_style=str(yapf_style), isort_config_file=str(isort_config))

	linter.process_file(outfile)

	with open(outfile, "r+b") as f:
		fix_encoding_pragma(f, remove=True, expected_pragma=b"# coding: utf-8")


def reformat_file(filename: PathLike, yapf_style: str, isort_config_file: str) -> int:
	"""
	Reformat the given file.

	:param filename:
	:param yapf_style: The name of the yapf style, or the path to the yapf style file.
	:param isort_config_file: The filename of the isort configuration file.
	"""

	old_isort_settings = isort.settings.CONFIG_SECTIONS.copy()

	try:
		isort.settings.CONFIG_SECTIONS["isort.cfg"] = ("settings", "isort")

		isort_config = isort.Config(settings_file=str(isort_config_file))
		r = yapf_isort.Reformatter(filename, yapf_style, isort_config)
		ret = r.run()
		r.to_file()

		return ret

	finally:
		isort.settings.CONFIG_SECTIONS = old_isort_settings


def process_multiple_notebooks(
		notebooks: Iterable[PathLike],
		outdir: PathLike,
		overwrite: bool = False,
		) -> int:
	"""
	Process multiple Jupyter notebooks for conversion into Python scripts.

	:param notebooks: An iterable of notebook filenames to process
	:param outdir: The directory to store the Python output in.
	:param overwrite: Whether to overwrite existing files.
	"""

	ret = 0
	outdir = PathPlus(outdir)

	for notebook in notebooks:
		notebook = PathPlus(notebook)
		outfile = outdir / f"{notebook.stem}.py"

		if outfile.is_file() and not overwrite:
			print(f"Info: Skipping existing file {outfile}")
		else:
			if notebook.is_file():
				print(f"Converting {notebook} to {outfile}")
				convert_notebook(notebook, outfile)
			else:
				print(f"{notebook} not found")
				ret |= 1

	return ret
