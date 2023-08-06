#!/usr/bin/env python3

import os
import sys
import hashlib
import atexit
import pydash as _

sys.path.insert(0, os.getcwd())

from utils.jsons import as_json
from utils.classes.JsonStore import JsonStore

class Cache(JsonStore):
	changed = False

	def __init__(self, path):
		super().__init__(path);
		atexit.register(lambda: self.save(path))

	def __call__(self, fn):
		def caching_wrapper(*args, **kwargs):
			key = self.hash(fn.__name__, args, kwargs)
			return self.fetch(key, lambda: fn(*args, **kwargs))
		return caching_wrapper

	def clear(self):
		super().clear()
		self.save()

	def save(self, path=False):
		if self.changed:
			super().save(path, False, False);
			
	def fetch(self, key, computation):
		hash = self.hash(key)
		if hash not in self.storage:
			self[hash] = computation()
		return self[hash]

	def hash(self, *value):
		try:
			value = as_json(value)
		except:
			value = str(value)
		return hashlib.md5(value.encode('utf-8')).hexdigest()

	def __str__(self):
		return f'<Cache Util {self.path}>'

def cached(method):
	class_name, method_name = method.__qualname__.split('.')

	def cached_method(*args, **kwargs):
		method_parent = method.__globals__[class_name]
		service_name = method_parent.name

		if not hasattr(method_parent, 'cache'):
			method_parent.init_cache()

		cache = method_parent.cache

		return cache.fetch([method_name, args, kwargs], lambda: method(*args, **kwargs))
	cached_method.is_cached = True
	cached_method.redirect = method

	return cached_method