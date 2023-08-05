import re
import pydash as _

def named_args_as_positional(args, param_definitions, service_name, method_name):
	import argparse
	parameter_names = _.map_(param_definitions, 'name')
	arg_list = '> <'.join(parameter_names)
	description = _.start_case(service_name) + f' Component: {method_name}(<{arg_list}>)'
	args_parser = argparse.ArgumentParser(usage=f'./{service_name}.py {method_name}', description=description)

	for definition in param_definitions:
		options = { 'nargs': '?' }
		default = definition.default

		if hasattr(default, '__name__'):
			if default is definition.empty:
				default = None

		if default is not None:
			options['help'] = f'(default: {default})'

		args_parser.add_argument(definition.name + '_pos', **options)
		args_parser.add_argument('--' + definition.name, **options)

	named_args, unknown_args = args_parser.parse_known_args(args)
	args = []

	for definition in param_definitions:
		name = definition.name
		value = _.get(named_args, name)
		if value is None:
			value = _.get(named_args, name + '_pos')

		if definition.kind == definition.VAR_POSITIONAL:
			args += unknown_args
		else:
			args.append(value)

	props_parser = argparse.ArgumentParser()
	properties = {}

	for arg in unknown_args:
		if arg.startswith('--'):
			arg_name, value = re.split(r'\s*=\s*', arg[2:].strip())
			properties[arg_name] = value.strip()
			args = _.without(args, arg)

	while (args[-1] is None) and len(args):
		args.pop()

	return { 'args': args, 'properties': properties }