import os
import json

def as_json(anything, pretty=True):
	indent = 4 if pretty else None 
	return json.dumps(anything, indent=indent)

def load_json(path, fallback=False):
	if os.path.isfile(path):
		with open(path, 'r') as json_file:
			content = json_file.read()
			return json.loads(content)
	return fallback or { 'error': f'Could not find {path}' }

def save_json(path, obj, pretty=True):
	indent = 4 if pretty else None 
	with open(path, 'w') as json_file:
		json.dump(obj, json_file, indent=indent)