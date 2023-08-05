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

# 3rd party
from pylint.checkers.base_checker import BaseChecker, BaseTokenChecker  # type: ignore
from pylint.utils import register_plugins  # type: ignore


def initialize(linter):
	"""
	Initialize linter with checkers in this package
	"""

	register_plugins(linter, __path__[0])  # type: ignore


__all__ = ("BaseChecker", "BaseTokenChecker", "initialize")
