#!/usr/bin/env python3

import re
import sys
from pathlib import Path
from utils.shell import shell_run

def install_cli():
	try:
		result = shell_run(['micro-components', 'get', 'version'])
	except:
		result = ''

	if re.match(r'\w+ [\d\.]+', result):
		print(' "micro-components" binary already installed. Skipping this part...')
	else:
		bin_folder = Path(sys.executable).parent
		builder_path = Path('./components/builder.py').resolve()
		result = shell_run(['ln', '-s', str(builder_path), bin_folder / 'micro-components'])
		print(' CLI "micro-components" created.')

if __name__ == '__main__':
	install_cli()