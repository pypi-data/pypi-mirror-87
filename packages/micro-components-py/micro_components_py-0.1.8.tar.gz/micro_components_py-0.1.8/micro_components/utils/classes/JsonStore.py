import os
import sys
import pydash as _

sys.path.insert(0, os.getcwd())

from utils.jsons import load_json, save_json

class JsonStore:
	changed = False
	storage = {}
	path = '';

	def __init__(self, path):
		self.path = path
		self.load()

	def load(self, path=False):
		self.path = path or self.path

		if os.path.exists(self.path):
			self.clear()
			self.storage = load_json(self.path)
		self.changed = False
		return self

	def save(self, path=False, storage=False, pretty=True):
		self.path = path or self.path
		if storage:
			self.storage = storage
		save_json(self.path, self.storage, pretty)
		self.changed = False
		return self

	def clear(self):
		self.storage = {}
		return self

	def __iter__(self):
		return iter(self.storage)

	def __getitem__(self, field):
		return _.get(self.storage, field, None)
		
	def __setitem__(self, field, value):
		_.set_(self.storage, field, value)
		self.changed = True

	def __delitem__(self, field):
		_.unset(self.storage, field)
		self.changed = True
		
	def __contains__(self, field):
		return bool(_.get(self.storage, field, False))

	def __len__(self):
		return _.size(self.storage)

	def __repr__(self):
		return repr(self.storage)