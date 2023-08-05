import os
import re
import sys
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

from pathlib import Path

def install_cli():
	try:
		result = os.system('micro-components get version').strip()
	except:
		result = ''

	if re.match(r'\w+ [\d\.]+', result):
		print(' "micro-components" binary already installed. Skipping this part...')
	else:
		bin_folder = Path(sys.executable).parent
		builder_path = Path('./micro_components/components/builder.py').resolve()
		cli_path = bin_folder / 'micro-components'
		result = os.system(f'ln -s {builder_path} {cli_path}').strip()
		print(' CLI "micro-components" created.')


class PreDevelopCommand(develop):
	def run(self):
		install_cli()
		develop.run(self)

class PreInstallCommand(install):
	def run(self):
		install_cli()
		install.run(self)

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "micro-components",
	version = "0.1.5",
	author = "Dan Borufka",
	author_email = "danborufka@gmail.com",
	description = "Lightweight library to create components that can automagically be used as either CLI or as native classes in other programming languages",
	license = "MIT",
	keywords = "components",
	url = "https://github.com/polygoat/micro-components-py",
	packages=find_packages(),
	install_requires=[
        "pydash",
        "termcolor",
		"colorama",
		"mako"
    ],
	include_package_data=True,
	cmdclass={
        'develop': PreDevelopCommand,
        'install': PreInstallCommand,
    },
	# long_description=read('README.md'),
	# long_description_content_type="text/markdown",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Topic :: Utilities",
		"License :: OSI Approved :: MIT License",
	],
)
