#!/usr/bin/env python3

import os
import re
import sys
import stat
from colorama import init as colorama_init, Fore, Style
import pydash as _
from pathlib import Path
from mako.template import Template

REPO_DIR = Path(__file__).resolve(strict=False).parents[1]
sys.path.insert(0, str(REPO_DIR))

from utils.classes.Component import Component

colorama_init(autoreset=True)

MAPPING = {
	'js': 'node',
	'javascript': 'node',
	'py': 'python'
}

ENDINGS = {
	'python': 'py',
	'node': 'js'
}

class Builder(Component):
	name = 'builder'
	version = 'Python 1.0.0'
	color = True

	def create(component_name, coding_language='python'):
		data = {
			'name': _.snake_case(component_name),
			'class_name': _.start_case(_.camel_case(component_name)).replace(' ', ''),
			'cwd': os.getcwd()
		}
		coding_language = _.get(MAPPING, coding_language, coding_language)
		with open(REPO_DIR / f'{coding_language}.component', 'r') as template_file:
			code_template = template_file.read()
			code_template = code_template.replace('<%= ', '${').replace(' %>', '}')
			render = Template(code_template).render
		
		file = render(**data)
		file_ending = ENDINGS[coding_language]
		file_path = f'./{data["name"]}.{file_ending}'

		with open(file_path, 'w') as component_file:
			component_file.write(file)
		
		os.chmod(file_path, 0o775)

		if Builder.color:
			print(Fore.GREEN + ' Component created.' + Style.RESET_ALL + ' Try it by running ' + Fore.YELLOW + f'{file_path} help')
		else:
			print(f'Component created. Try it by running {file_path} help')

Builder.export_as_cli()