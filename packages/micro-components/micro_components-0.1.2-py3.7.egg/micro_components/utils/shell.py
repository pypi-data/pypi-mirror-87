import re
import os
import json
import subprocess

def shell_run(script, verbose=False):
	out = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = out.communicate()
	output = (stdout or stderr or b'').strip()

	try:		output = output.decode("utf-8")
	except:		...

	try:				return json.loads(output)
	except Exception:	return output