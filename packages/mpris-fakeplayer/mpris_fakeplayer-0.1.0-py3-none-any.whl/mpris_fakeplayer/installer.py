
import sys
import pkgutil

from pathlib import PosixPath
from argparse import Action

from . import APP_NAME

class Installer(Action):

	RESOURCE = 'resources/' + APP_NAME + '.service'
	TARGET = '/usr/lib/systemd/user/' + APP_NAME + '.service'

	def __call__(self, *args):
		executable = PosixPath(sys.argv[0]).resolve()

		data = pkgutil\
			.get_data(
				__package__,
				self.RESOURCE
			)\
			.decode()\
			.replace(APP_NAME, executable.as_posix())

		with open(self.TARGET, 'w') as f:
			f.write(data)

		sys.exit(0)

