import os
import re
import sys
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

from pathlib import Path
from micro_components.utils.shell import shell_run
from micro_components.setup import install_cli

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
	version = "0.1.3",
	author = "Dan Borufka",
	author_email = "danborufka@gmail.com",
	description = "Lightweight library to create components that can automagically be used as either CLI or as native classes in other programming languages",
	license = "MIT",
	keywords = "components",
	url = "https://github.com/polygoat/micro-components-py",
	packages=find_packages(),
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
