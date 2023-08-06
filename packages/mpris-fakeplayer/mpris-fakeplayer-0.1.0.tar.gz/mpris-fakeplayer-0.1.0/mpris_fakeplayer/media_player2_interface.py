
from dbus_next.constants import (
	PropertyAccess
)
from dbus_next.service import (
	ServiceInterface,
	method,
	dbus_property
)

from .logger import logger

class MediaPlayer2Interface(ServiceInterface):

	INTERFACE = 'org.mpris.MediaPlayer2'

	def __init__(self):
		super().__init__(self.INTERFACE)

	@method()
	def Raise(self):
		logger.debug('Raise')

	@method()
	def Quite(self):
		logger.debug('Quite')

	@dbus_property(PropertyAccess.READ)
	def Identity(self) -> 's':
		return 'FakePlayer'

	@dbus_property(PropertyAccess.READ)
	def CanQuit(self) -> 'b':
		return False

	@dbus_property(PropertyAccess.READ)
	def Fullscreen(self) -> 'b':
		return False

	@dbus_property(PropertyAccess.READ)
	def CanSetFullscreen(self) -> 'b':
		return False

	@dbus_property(PropertyAccess.READ)
	def CanRaise(self) -> 'b':
		return True

	@dbus_property(PropertyAccess.READ)
	def HasTrackList(self) -> 'b':
		return False

	@dbus_property(PropertyAccess.READ)
	def DesktopEntry(self) -> 's':
		return None

	@dbus_property(PropertyAccess.READ)
	def SupportedUriSchemes(self) -> 'as':
		return []

	@dbus_property(PropertyAccess.READ)
	def SupportedMimeTypes(self) -> 'as':
		return []
