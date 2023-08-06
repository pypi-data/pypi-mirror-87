
import sys
import logging

from importlib import util

from . import APP_NAME

class LoggerBuilder():

	def __init__(self):
		self.logger = logging.getLogger(APP_NAME)
		self.logger.setLevel(logging.DEBUG)

		self._init_journal()
		self._init_console()

	def _init_journal(self):
		handler = self._handler_journal
		if (handler):
			self.logger.addHandler(handler)

	@property
	def _handler_journal(self):
		return self._handler_systemd\
			or self._handler_cysystemd

	@property
	def _handler_systemd(self):
		if (util.find_spec('systemd')):
			from systemd import journal

			return journal.JournalHandler(
				SYSLOG_IDENTIFIER = self.logger.name
			)

	@property
	def _handler_cysystemd(self):
		if (util.find_spec('cysystemd')):
			from cysystemd import journal

			return journal.JournaldLogHandler()

	def _init_console(self):
		self.logger.addHandler(self._handler_console)

	@property
	def _handler_console(self):
		handler = logging.StreamHandler()
		handler.setLevel(logging.WARNING)
		handler.setFormatter(self._formatter)

		return handler

	@property
	def _formatter(self):
		pattern = '%(levelname)s: %(message)s'
		formatter = logging.Formatter(pattern)

		if (util.find_spec('colorlog')):
			import colorlog
			formatter = colorlog.ColoredFormatter(
				'%(log_color)s' + pattern
			)

		return formatter


logger = LoggerBuilder().logger

def _excepthook(exctype, exception, traceback):
	logger.error(exception)

	import datetime
	date = datetime.datetime.now().isoformat(timespec = 'seconds')

	from pathlib import PosixPath
	dump = PosixPath('/tmp/' + APP_NAME + '/' + date + '.dump')

	if (not dump.parent.exists()):
		dump.parent.mkdir()

	with open(dump, 'w') as f:
		f.write(str(sys.argv) + '\n\n')
		from traceback import print_tb
		print_tb(traceback, file = f)
		f.write('\n' + str(exception))

sys.excepthook = _excepthook
