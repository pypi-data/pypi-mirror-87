"""
Ensure pointless statements in scripts are converted
into print function calls
"""

#    Copyright (C) 2020 Dominic Davis-Foster

#    Based on pylint
#    Copyright (c) 2006-2016 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
#    Copyright (c) 2008 Fabrice Douchant <Fabrice.Douchant@logilab.fr>
#    Copyright (c) 2009 Mads Kiilerich <mads@kiilerich.com>
#    Copyright (c) 2009 Vincent
#    Copyright (c) 2010 Daniel Harding <dharding@gmail.com>
#    Copyright (c) 2010 Julien Jehannet <julien.jehannet@logilab.fr>
#    Copyright (c) 2011-2014 Google, Inc.
#    Copyright (c) 2012 David Pursehouse <david.pursehouse@sonymobile.com>
#    Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
#    Copyright (c) 2012 JT Olds <jtolds@xnet5.com>
#    Copyright (c) 2012 Kevin Jing Qiu <kevin.jing.qiu@gmail.com>
#    Copyright (c) 2012-2014 Google, Inc.
#    Copyright (c) 2013 buck@yelp.com <buck@yelp.com>
#    Copyright (c) 2013-2014 Google, Inc.
#    Copyright (c) 2013-2020 Claudiu Popa <pcmanticore@gmail.com>
#    Copyright (c) 2014 Alexandru Coman <fcoman@bitdefender.com>
#    Copyright (c) 2014 Arun Persaud <arun@nubati.net>
#    Copyright (c) 2014 Brett Cannon <brett@python.org>
#    Copyright (c) 2014 Dan Goldsmith <djgoldsmith@googlemail.com>
#    Copyright (c) 2014 Daniel Harding <dharding@living180.net>
#    Copyright (c) 2014 Ricardo Gemignani <ricardo.gemignani@gmail.com>
#    Copyright (c) 2014, 2016-2020 Claudiu Popa <pcmanticore@gmail.com>
#    Copyright (c) 2014-2015 Michal Nowikowski <godfryd@gmail.com>
#    Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
#    Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
#    Copyright (c) 2015 Cosmin Poieana <cmin@ropython.org>
#    Copyright (c) 2015 Dmitry Pribysh <dmand@yandex.ru>
#    Copyright (c) 2015 Florian Bruhin <me@the-compiler.org>
#    Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
#    Copyright (c) 2015 Michael Kefeder <oss@multiwave.ch>
#    Copyright (c) 2015 Mihai Balint <balint.mihai@gmail.com>
#    Copyright (c) 2015 Nick Bastin <nick.bastin@gmail.com>
#    Copyright (c) 2015 Radu Ciorba <radu@devrandom.ro>
#    Copyright (c) 2015 Simu Toni <simutoni@gmail.com>
#    Copyright (c) 2015 Stephane Wirtel <stephane@wirtel.be>
#    Copyright (c) 2015 Steven Myint <hg@stevenmyint.com>
#    Copyright (c) 2015-2016 Florian Bruhin <me@the-compiler.org>
#    Copyright (c) 2016 Alan Evangelista <alanoe@linux.vnet.ibm.com>
#    Copyright (c) 2016 Alex Jurkiewicz <alex@jurkiewi.cz>
#    Copyright (c) 2016 Elias Dorneles <eliasdorneles@gmail.com>
#    Copyright (c) 2016 Florian Bruhin <git@the-compiler.org>
#    Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
#    Copyright (c) 2016 Jakub Wilk <jwilk@jwilk.net>
#    Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
#    Copyright (c) 2016 Yannack <yannack@users.noreply.github.com>
#    Copyright (c) 2016, 2018 Jakub Wilk <jwilk@jwilk.net>
#    Copyright (c) 2016, 2019 Ashley Whetter <ashley@awhetter.co.uk>
#    Copyright (c) 2016-2017 Łukasz Rogalski <rogalski.91@gmail.com>
#    Copyright (c) 2017 Daniel Miller <millerdev@gmail.com>
#    Copyright (c) 2017 danields <danields761@gmail.com>
#    Copyright (c) 2017 Jacques Kvam <jwkvam@gmail.com>
#    Copyright (c) 2017 Ned Batchelder <ned@nedbatchelder.com>
#    Copyright (c) 2017 Pierre Sassoulas <pierre.sassoulas@cea.fr>
#    Copyright (c) 2017 Roman Ivanov <me@roivanov.com>
#    Copyright (c) 2017 ttenhoeve-aa <ttenhoeve@appannie.com>
#    Copyright (c) 2017, 2019 hippo91 <guillaume.peillex@gmail.com>
#    Copyright (c) 2017-2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
#    Copyright (c) 2017-2018 Hugo <hugovk@users.noreply.github.com>
#    Copyright (c) 2017-2018 Ville Skyttä <ville.skytta@iki.fi>
#    Copyright (c) 2017-2019 hippo91 <guillaume.peillex@gmail.com>
#    Copyright (c) 2018 Chris Lamb <chris@chris-lamb.co.uk>
#    Copyright (c) 2018 Gary Tyler McLeod <mail@garytyler.com>
#    Copyright (c) 2018 glmdgrielson <32415403+glmdgrielson@users.noreply.github.com>
#    Copyright (c) 2018 Jason Owen <jason.a.owen@gmail.com>
#    Copyright (c) 2018 kapsh <kapsh@kap.sh>
#    Copyright (c) 2018 Lucas Cimon <lucas.cimon@gmail.com>
#    Copyright (c) 2018 Matus Valo <matusvalo@users.noreply.github.com>
#    Copyright (c) 2018 Mike Frysinger <vapier@gmail.com>
#    Copyright (c) 2018 Natalie Serebryakova <natalie.serebryakova@Natalies-MacBook-Pro.local>
#    Copyright (c) 2018 Nick Drozd <nicholasdrozd@gmail.com>
#    Copyright (c) 2018 Randall Leeds <randall@bleeds.info>
#    Copyright (c) 2018 Sergei Lebedev <185856+superbobry@users.noreply.github.com>
#    Copyright (c) 2018 SergeyKosarchuk <sergeykosarchuk@gmail.com>
#    Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
#    Copyright (c) 2018 Steven M. Vascellaro <svascellaro@gmail.com>
#    Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
#    Copyright (c) 2018 Yuval Langer <yuvallanger@mail.tau.ac.il>
#    Copyright (c) 2018, 2020 Anthony Sottile <asottile@umich.edu>
#    Copyright (c) 2018-2019 Ashley Whetter <ashley@awhetter.co.uk>
#    Copyright (c) 2018-2019 Nick Drozd <nicholasdrozd@gmail.com>
#    Copyright (c) 2018-2019 Ville Skyttä <ville.skytta@iki.fi>
#    Copyright (c) 2018-2020 Pierre Sassoulas <pierre.sassoulas@gmail.com>
#    Copyright (c) 2019 Andres Perez Hortal <andresperezcba@gmail.com>
#    Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
#    Copyright (c) 2019 Bruno P. Kinoshita <kinow@users.noreply.github.com>
#    Copyright (c) 2019 Dan Hemberger <846186+hemberger@users.noreply.github.com>
#    Copyright (c) 2019 Daniel Draper <Germandrummer92@users.noreply.github.com>
#    Copyright (c) 2019 Fantix King <fantix@uchicago.edu>
#    Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
#    Copyright (c) 2019 Hugues <hugues.bruant@affirm.com>
#    Copyright (c) 2019 jab <jab@users.noreply.github.com>
#    Copyright (c) 2019 Janne Rönkkö <jannero@users.noreply.github.com>
#    Copyright (c) 2019 Nicolas Dickreuter <dickreuter@gmail.com>
#    Copyright (c) 2019 Nikita Sobolev <mail@sobolevn.me>
#    Copyright (c) 2019 Niko Wenselowski <niko@nerdno.de>
#    Copyright (c) 2019 Oisín Moran <OisinMoran@users.noreply.github.com>
#    Copyright (c) 2019 Peter Kolbus <peter.kolbus@gmail.com>
#    Copyright (c) 2019 Pierre Sassoulas <pierre.sassoulas@gmail.com>
#    Copyright (c) 2019 Robert Schweizer <robert_schweizer@gmx.de>
#    Copyright (c) 2019 syutbai <syutbai@gmail.com>
#    Copyright (c) 2019 Thomas Hisch <t.hisch@gmail.com>
#    Copyright (c) 2019 Trevor Bekolay <tbekolay@gmail.com>
#    Copyright (c) 2019 Ville Skyttä <ville.skytta@iki.fi>
#    Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
#    Copyright (c) 2020 anubh-v <anubhav@u.nus.edu>
#    Copyright (c) 2020 Anubhav <35621759+anubh-v@users.noreply.github.com>
#    Copyright (c) 2020 Benny <benny.mueller91@gmail.com>
#    Copyright (c) 2020 bernie gray <bfgray3@users.noreply.github.com>
#    Copyright (c) 2020 Gabriel R Sezefredo <g@briel.dev>
#    Copyright (c) 2020 Pierre Sassoulas <pierre.sassoulas@gmail.com>
#
#    See https://github.com/PyCQA/pylint/blob/master/COPYING for more details.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

# TODO: not all statements that need to be made into prints are being picked up.
#  Include a list of those and convert manually

# stdlib
import contextlib
import pathlib
import sys
import warnings

# 3rd party
from pylint import reporters  # type: ignore
from pylint.lint.pylinter import PyLinter  # type: ignore
from pylint.utils import utils  # type: ignore

# this package
from notebook2script import pointless_checker

__all__ = ["Pointless", "fix_import_path"]


class Pointless(PyLinter):

	def __init__(self):
		super().__init__()
		self.load_default_plugins()
		self.enable("pointless-statement")
		self.initialize()
		self.statements = []

	def load_default_plugins(self):
		pointless_checker.initialize(self)
		reporters.initialize(self)
		# Make sure to load the default reporter, because
		# the option has been set before the plugins had been loaded.
		if not self.reporter:
			self._load_reporter()

	def process_file(self, filename):
		self.statements = []

		with fix_import_path([filename]):
			self._check_files(self.get_ast, self._iterate_file_descrs([filename]))

		filename = pathlib.Path(filename)
		file_lines = filename.read_text().splitlines()

		for node in self.statements:

			if node.tolineno != node.lineno:
				warnings.warn("Currently unable to convert this statement")

			else:
				value = node.value.as_string()
				col = node.col_offset
				lineno = node.lineno - 1

				line = file_lines[lineno]
				line_pre_statement = line[:col]
				line_post_statement = line[col + len(value):]
				# print(f"{line_pre_statement}print({value}){line_post_statement}")
				file_lines[lineno] = f"{line_pre_statement}print({value}){line_post_statement}"

		if file_lines[-1]:
			# ensure there's a newline at the end
			file_lines.append('')

		# print("\n".join(file_lines))
		filename.write_text('\n'.join(file_lines))

	def add_message(self, msgid, line=None, node=None, args=None, confidence=None, col_offset=None):
		"""Adds a message given by ID or name.

		If provided, the message string is expanded using args.

		AST checkers must provide the node argument (but may optionally
		provide line if the line number is different), raw and token checkers
		must provide the line argument.
		"""

		self.statements.append(node)
		# super().add_message(msgid, line, node, args, confidence, col_offset)


def _patch_sys_path(args):
	original = list(sys.path)
	changes = []
	seen = set()
	for arg in args:
		path = utils.get_python_path(arg)
		if path not in seen:
			changes.append(path)
			seen.add(path)

	sys.path[:] = changes + sys.path
	return original


@contextlib.contextmanager
def fix_import_path(args):
	"""
	Prepare sys.path for running the linter checks.

	Within this context, each of the given arguments is importable.
	Paths are added to sys.path in corresponding order to the arguments.
	We avoid adding duplicate directories to sys.path.
	`sys.path` is reset to its original value upon exiting this context.
	"""

	original = _patch_sys_path(args)
	try:
		yield
	finally:
		sys.path[:] = original
