#!/usr/bin/env python3

import os
import re
import sys
import json
import types
import atexit
import inspect
import pydash as _
from io import StringIO
from pathlib import Path
from termcolor import colored
from colorama import init as colorama_init, Fore, Style

cwd = Path(__file__)
sys.path.insert(0, str(cwd.parents[2]))

from utils.classes.Cache import Cache
from utils.classes.Hookable import Hookable

from utils.jsons import as_json
from utils.shell import shell_run
from utils.funcs import named_args_as_positional
from utils.formats import string_to_any

ENGINES = {
	'py':   'python',
	'js':   'node',
	'sh':   'shell',
	'java': 'java'
}

colorama_init(autoreset=True)

def respond(anything):
    return json.dumps(anything, indent=4)

def has_named_args(args):
	if re.match(r'(^| )\-\-\w+', ' '.join(args)):
		return True
	return False

class Component(Hookable):
	name = ''
	called_from_cli = False

	registered = []

	description = ''
	is_component = True
	is_cached = False
	has_cache = False


	def __init__(self, options, extras=None):
		self.init(options)
		Component.registered.append(self)

		self.engine = 'python'

		if self.has_cache or self.is_cached:
			self.cache = Cache(f'data/caches/{self.name}.cache.json')

		Component.trigger('spawn', [self])
		return self.trigger('spawn', [self])

	def init(self, options=None):
		if not isinstance(self, Component):
			options = self
			self = Component.instance

		if not options:
			options = {}

		if isinstance(options, str):
			options = json.loads(options)

		for key, value in options.items():
			setattr(self, key, value)

		Component.trigger('init', [options])
		self.trigger('init', [self, options])
		return self

	@staticmethod
	def from_cli(path, extras=None):
		return ComponentCLI(path, extras)
		
	@classmethod
	def init_cache(self):
		self.cache = Cache(f'data/caches/{self.name}.cache.json')
		self.has_cache = True

	@classmethod
	def clear_cache(self):
		self.cache.clear()

	def help(self):
		self.engine = 'python'
		component_props = dir(Component) + ['[']

		callables = []
		props = []

		properties = dir(self)
		properties = _.without(properties, *component_props)

		properties = Component.trigger('help', [properties], properties)

		for prop in properties:
			if prop[0:2] != '__':
				attribute = getattr(self, prop)
				entry = {'name': prop }
				if callable(attribute):
					if hasattr(attribute, 'redirect'):
						attribute = attribute.redirect
					entry['params'] = str(inspect.signature(attribute))
					entry['params'] = re.sub(r' ?self, ?', '', entry['params'])
					entry['params'] = re.sub(r'(=[^,)]+)', Style.DIM + r'\1' + Style.RESET_ALL, entry['params'])
					entry['params'] = re.sub(r'([()])', Fore.YELLOW + r'\1' + Style.RESET_ALL, entry['params'])
					callables.append(entry)
				else:
					entry['value'] = attribute
					props.append(entry)	

		print(colored(f' {_.start_case(self.name)} Component', attrs=['bold']))
		if self.description:
			print(' ' + self.description + '\n')

		if callables:
			print('\t' + colored('Available methods:', attrs=['underline']))
			print('')
			for method in callables:
				print(f'\t\t.{method["name"]}{method["params"]}')

		if props:
			print('\n\t' + colored('Available properties:', attrs=['underline']))
			print('')
			for prop in props:
				print(f'\t\t.{prop["name"]} ' + Style.DIM + f'(default {prop["value"]})')

		print('')
		return ''

	def cli_commands(self, *arguments):
		commands = list(arguments)

		if ',' in commands:
			next_comma_pos = commands.index(',') - 1
		else:
			next_comma_pos = len(commands)

		entire_log = []
		i = 0

		if commands[-1] == ']':
			commands = commands[:-1]

		while len(commands):
			command = commands.pop(0)
			params = commands[:next_comma_pos]
			commands = commands[next_comma_pos:]

			std_out = sys.stdout
			sys.stdout = output = StringIO()
			Component.instance.call_from_cli(Component.instance, command, params)
			sys.stdout = std_out

			output = output.getvalue().strip()
			entire_log.append(output)

			if ',' in commands:
				next_comma_pos = commands.index(',') - 1
			else:
				next_comma_pos = len(commands)

			i += 1
		
		return { 'results': entire_log };

	def get(self, prop):
		return getattr(self, prop)

	def set(self, prop, value):
		setattr(self, prop, value)

	def get_classname(self, component_name):
		return _.upper_first(_.camel_case(component_name or self.name))

	def call_from_cli(self, command, args, verbose=True):
		command = command.replace('-', '_')

		if Component.instance:
			self = Component.instance

		if hasattr(self, command):
			command = getattr(self, command)

			method_container = command

			if hasattr(command, 'redirect'):
				method_container = command.redirect

			params = inspect.signature(method_container).parameters.values()
			is_static = isinstance(method_container, types.FunctionType) and list(params)[0].name != 'self'

			if has_named_args(args):
				named = named_args_as_positional(args, params, self.name, method_container.__name__)
				args = named['args']
				named['properties'] = _.map_values(named['properties'], string_to_any)
				self.init(named['properties'])

			last_param = list(params)[-1]
			is_consuming_rest = last_param.kind == last_param.VAR_POSITIONAL

			if not is_consuming_rest and len(args) > len(params):
				result = { 'error': f'Wrong number of arguments passed to {command.__name__}: expected {len(params)} instead of {len(args)}.' }
			else:
				args = list(map(string_to_any, args))
					
				if not is_static:
					args.insert(0, self)

				self.called_from_cli = True
				command.as_cli = True

				result = command(*args)
		else:
			result = { 'error': f'{self.name} has no method {command}.' }

		if verbose:
			if result:
				print(respond(result))
		else:
			return result

	@classmethod
	def export_as_cli(self):
		Component.instance = self
		is_imported = self.__module__ != '__main__'
		if not is_imported:
			args = sys.argv[1:]

			if len(args):
				command = args.pop(0)
				setattr(self, '[', self.cli_commands)
				self.call_from_cli(self, command, args, True)
		return self

	def __repr__(self):
		return str(self.__dict__)

	def __str__(self):
		out = 'Component {'
		for prop in dir(self):
			if not prop.startswith('__'):
				value = getattr(self, prop)
				out += f'\n\t{prop}: {str(value)}'
		out += '\n}'
		return out

class ComponentCLIProp:
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent
		self.value = False

	def get(self):
		repr(self)
		return self.value

	def __call__(self, *params):
		args = []

		for param in params:
			if isinstance(param, (dict, list)):
				args.append(as_json(param, pretty=False))
			else:
				args.append(param)

		command = [self.parent.path, self.name, *args]
		
		if self.parent.is_cached:
			cache_key = self.parent.trigger('create_cache_key', [command]) or command
			return self.parent.cache.fetch(cache_key, lambda: string_to_any(shell_run(command)))

		result = shell_run(command)
		result = string_to_any(result)
		return result

	def __repr__(self):
		param = self.name + ''
		self.name = 'get'
		self.value = self.__call__(param)
		return repr(self.value)

class ComponentCLI(Hookable):
	def __init__(self, name, options={}):
		self.path = name
		
		name_parts = os.path.splitext(os.path.basename(name))
		name = name_parts[0]
		file_format = name_parts[1]

		self.name = name
		self.engine = ENGINES[file_format[1:]]
		self.format = file_format
		self.is_cached = _.get(options, 'cached', False)
		self.cache = Cache(f'data/caches/{name}.cache.json')
	
	def __getattr__(self, name):
		if name in dir(self):
			return getattr(self, name)
		return ComponentCLIProp(name, self)

def cached(method):
	class_name, method_name = method.__qualname__.split('.')

	def cached_method(*args, **kwargs):
		method_parent = method.__globals__[class_name]
		component_name = method_parent.name

		if not hasattr(method_parent, 'cache'):
			method_parent.init_cache()

		cache = method_parent.cache

		Component.trigger('cache', [method_name, args, kwargs])
		return cache.fetch([method_name, args, kwargs], lambda: method(*args, **kwargs))
	cached_method.is_cached = True
	cached_method.redirect = method

	return cached_method