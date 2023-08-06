
APP_NAME = 'mpris-fakeplayer'

import asyncio
import signal

from dbus_next.aio import MessageBus

from .installer import Installer

from .media_player2_interface import MediaPlayer2Interface
from .media_player2_player_interface import MediaPlayer2PlayerInterface

class MprisFakePlayer():

	NAME = 'org.mpris.MediaPlayer2.FakePlayer'
	PATH = '/org/mpris/MediaPlayer2'

	def __init__(self):
		self.loop = None
		self.future = None

		self.bus = None
		self.player2 = MediaPlayer2Interface()
		self.player2_player = MediaPlayer2PlayerInterface()

	async def play(self):
		signal.signal(signal.SIGINT, self.stop)
		signal.signal(signal.SIGTERM, self.stop)

		self.bus = await MessageBus().connect()

		self.bus.export(MprisFakePlayer.PATH, self.player2)
		self.bus.export(MprisFakePlayer.PATH, self.player2_player)

		await self.bus.request_name(MprisFakePlayer.NAME)

		self.loop = asyncio.get_event_loop()
		self.future = self.loop.create_future()
		await self.future

		self.player2_player.Stop()
		await self.bus.release_name(MprisFakePlayer.NAME)

	def stop(self, signal_num = 2, frame = None):
		self.loop.call_soon_threadsafe(self.future.set_result, True)

def main():
	import argparse

	parser = argparse.ArgumentParser(
		prog = APP_NAME,
	)
	parser.add_argument(
		'--install-service',
		dest = 'install',
		action = Installer,
		nargs = 0,
		default = False,
		required = False,
		help = 'install systemd user service',
	)
	parser.parse_args()

	fake_player = MprisFakePlayer()
	asyncio.run(fake_player.play())
