################################################################################
#                                                                              #
#    Copyright (C) 2020 Dominic Davis-Foster                                   #
#    Based on pylint                                                           #
#    See notebook2script/pointless.py for full copyright information           #
#                                                                              #
#    This program is free software; you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License version 2 as         #
#    published by the Free Software Foundation.                                #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with this program; if not, write to the Free Software               #
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.                 #
#                                                                              #
################################################################################

# stdlib
from typing import Dict, Tuple

# 3rd party
import astroid  # type: ignore
import astroid.bases  # type: ignore
import astroid.scoped_nodes  # type: ignore
from pylint import interfaces  # type: ignore
from pylint.checkers import utils  # type: ignore
from pylint.checkers.base_checker import BaseChecker  # type: ignore

__all__ = ["BasicChecker", "register"]


class BasicChecker(BaseChecker):
	"""checks for :
	* doc strings
	* number of arguments, local variables, branches, returns and statements in
	functions, methods
	* required module attributes
	* dangerous default values as arguments
	* redefinition of function / method / class
	* uses of the global statement
	"""

	__implements__ = interfaces.IAstroidChecker

	msgs: Dict[str, Tuple[str, str, str]] = {
			"W0104": (
					"Statement seems to have no effect",
					"pointless-statement",
					"Used when a statement doesn't have (or at least seems to) any effect.",
					),
			"W0105": (
					"String statement has no effect",
					"pointless-string-statement",
					"Used when a string is used as a statement (which of course "
					"has no effect). This is a particular case of W0104 with its "
					"own message so you can easily disable it if you're using "
					"those strings as documentation, instead of comments.",
					),
			"W0106": (
					"Expression '%s' is assigned to nothing",
					"expression-not-assigned",
					"Used when an expression that is not a function call is assigned "
					"to nothing. Probably something else was intended.",
					),
			}

	reports = ()

	@utils.check_messages("pointless-statement", "pointless-string-statement", "expression-not-assigned")
	def visit_expr(self, node) -> None:
		"""
		Check for various kinds of statements without effect.
		"""

		expr = node.value

		if isinstance(expr, astroid.Const) and isinstance(expr.value, str):
			# treat string statement in a separated message
			# Handle PEP-257 attribute docstrings.
			# An attribute docstring is defined as being a string right after
			# an assignment at the module level, class level or __init__ level.
			scope = expr.scope()
			if isinstance(scope, (astroid.ClassDef, astroid.Module, astroid.FunctionDef)):
				if isinstance(scope, astroid.FunctionDef) and scope.name != "__init__":
					pass
				else:
					sibling = expr.previous_sibling()
					if (
							sibling is not None and sibling.scope() is scope
							and isinstance(sibling, (astroid.Assign, astroid.AnnAssign))
							):
						return
			self.add_message("pointless-string-statement", node=node)
			return

		# Ignore if this is :
		# * a direct function call
		# * the unique child of a try/except body
		# * a yield statement
		# * an ellipsis (which can be used on Python 3 instead of pass)
		# warn W0106 if we have any underlying function call (we can't predict
		# side effects), else pointless-statement
		if (
				isinstance(expr, (astroid.Yield, astroid.Await, astroid.Ellipsis, astroid.Call))
				or (isinstance(node.parent, astroid.TryExcept) and node.parent.body == [node])
				or (isinstance(expr, astroid.Const) and expr.value is Ellipsis)
				):
			return
		if any(expr.nodes_of_class(astroid.Call)):
			self.add_message("expression-not-assigned", node=node, args=expr.as_string())
		else:
			self.add_message("pointless-statement", node=node)


def register(linter) -> None:
	"""
	required method to auto register this checker
	"""

	linter.register_checker(BasicChecker(linter))
