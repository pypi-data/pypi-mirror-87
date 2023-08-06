
from dbus_next.constants import (
	PropertyAccess
)
from dbus_next.service import (
	ServiceInterface,
	method,
	dbus_property
)

from .logger import logger

class MediaPlayer2PlayerInterface(ServiceInterface):

	INTERFACE = 'org.mpris.MediaPlayer2.Player'

	STATUS_PLAYING = 'Playing'
	STATUS_STOPPED = 'Stopped'

	def __init__(self):
		super().__init__(self.INTERFACE)

		self.status = self.STATUS_PLAYING

	@method()
	def Play(self):
		self.status = self.STATUS_PLAYING

	@method()
	def Stop(self):
		self.status = self.STATUS_STOPPED

	@method()
	def Next(self):
		logger.debug('Next')

	@method()
	def Previous(self):
		logger.debug('Previous')

	@method()
	def Pause(self):
		logger.debug('Pause')

	@method()
	def PlayPause(self):
		logger.debug('PlayPause')

	@method()
	def Seek(self, offset: 'x'):
		logger.debug(str(['Seek', offset]))

	@method()
	def SetPosition(self, track_id: 'o', position: 'x'):
		logger.debug(str(['SetPosition', track_id, position]))

	@method()
	def OpenUri(self, uri: 's'):
		logger.debug(str(['OpenUri', uri]))

	@dbus_property(PropertyAccess.READ)
	def PlaybackStatus(self) -> 's':
		return self.status

	@dbus_property(PropertyAccess.READWRITE)
	def LoopStatus(self) -> 's':
		return 'None'

	@LoopStatus.setter
	def LoopStatus(self, status: str):
		logger.debug(str(['LoopStatus', status]))

	@dbus_property(PropertyAccess.READWRITE)
	def Rate(self) -> 'd':
		return 1.0

	@Rate.setter
	def Rate(self, rate):
		logger.debug(str(['Rate', rate]))

	@dbus_property(PropertyAccess.READWRITE)
	def Shuffle(self) -> 'b':
		return False

	@Shuffle.setter
	def Shuffle(self, shuffle):
		logger.debug(str(['Shuffle', shuffle]))

	@dbus_property(PropertyAccess.READ)
	def Metadata(self) -> 'a{sv}':
		return {}

	@dbus_property(PropertyAccess.READWRITE)
	def Volume(self) -> 'd':
		return 1.0

	@Volume.setter
	def Volume(self, volume):
		logger.debug(str(['Volume', volume]))

	@dbus_property(PropertyAccess.READ)
	def Position(self) -> 'x':
		return 0

	@dbus_property(PropertyAccess.READ)
	def MinimumRate(self) -> 'd':
		return 1.0

	@dbus_property(PropertyAccess.READ)
	def MaximumRate(self) -> 'd':
		return 1.0

	@dbus_property(PropertyAccess.READ)
	def CanGoNext(self) -> 'b':
		return False

	@dbus_property(PropertyAccess.READ)
	def CanGoPrevious(self) -> 'b':
		return False

	@dbus_property(PropertyAccess.READ)
	def CanPlay(self) -> 'b':
		return True

	@dbus_property(PropertyAccess.READ)
	def CanPause(self) -> 'b':
		return False

	@dbus_property(PropertyAccess.READ)
	def CanSeek(self) -> 'b':
		return False

	@dbus_property(PropertyAccess.READ)
	def CanControl(self) -> 'b':
		return True

	@property
	def status(self):
		return self.__status

	@status.setter
	def status(self, status: str):
		self.__status = str(status)

		self.emit_properties_changed({
			'PlaybackStatus': self.PlaybackStatus
		})

		logger.debug(self.PlaybackStatus)

	def set_status(self, status: str):
		self.status = status

		return self
