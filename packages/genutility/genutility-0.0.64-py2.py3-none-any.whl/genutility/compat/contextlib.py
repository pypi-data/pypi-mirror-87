from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

try:
	from contextlib import ExitStack
except ImportError:
	from contextlib2 import ExitStack

try:
	from contextlib import nullcontext  # pylint: disable=no-name-in-module

except ImportError:

	if TYPE_CHECKING:
		from typing import Optional, TypeVar
		T = TypeVar("T")

	try:
		from contextlib import AbstractContextManager
	except ImportError:
		AbstractContextManager = object

	class nullcontext(AbstractContextManager):

		""" A context manager which doesn't do anything except return its argument.
			Kind of like an identity function for contexts, useful as default argument.
		"""

		def __init__(self, enter_result=None):
			# type: (Optional[T], ) -> None

			self.enter_result = enter_result

		def __enter__(self):
			# type: () -> Optional[T]

			return self.enter_result

		def __exit__(self, exc_type, exc_value, traceback):
			pass
