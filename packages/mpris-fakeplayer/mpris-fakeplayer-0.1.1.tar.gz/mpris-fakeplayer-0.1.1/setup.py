
import setuptools

from mpris_fakeplayer import APP_NAME

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = APP_NAME,
	version = "0.1.1",
	python_requires = '>=3.7',
	install_requires = [
		'dbus-next>=0.1.3',
	],
	extra_require = [
		'cysystemd>=0.16.2', # systemd
		'colorlog>=3.1.1',
	],
	entry_points = {
		'console_scripts': [
			APP_NAME + ' = mpris_fakeplayer:main',
		],
	},
	package_data={
		'': ['resources/' + APP_NAME + '.service'],
	},
	author = "hxss",
	author_email = "hxss@ya.ru",
	description = "Fake mpris player for activating bluez avrcp volume control",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	license = 'MIT',
	url = "https://gitlab.com/hxss-linux/mpris-fakeplayer",
	packages = setuptools.find_packages(),
	keywords = ['mpris', 'avrcp', 'bluez', 'player'],
	classifiers = [
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Topic :: Utilities",
	],
)
