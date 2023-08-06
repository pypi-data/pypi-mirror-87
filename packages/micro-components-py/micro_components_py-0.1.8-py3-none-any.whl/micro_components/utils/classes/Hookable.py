import inspect
import functools

class Hookable:
	hooks = {}

	@classmethod
	def on(cls, event_label, method):
		if event_label not in cls.hooks:
			cls.hooks[event_label] = []

		cls.hooks[event_label].append(method)

	@classmethod
	def trigger(cls, event_label, parameters=None, fallback=False):
		if not parameters:
			parameters = []
		if event_label in cls.hooks:
			result = None
			for hook in cls.hooks[event_label]:
				result = hook(*parameters)
				parameters[0] = result
			return result
		return fallback

def get_defining_class(method):
	if isinstance(method, functools.partial):
		return get_class_that_defined_method(method.func)
	if inspect.ismethod(method) or (inspect.isbuiltin(method) and getattr(method, '__self__', None) is not None and getattr(method.__self__, '__class__', None)):
		for cls in inspect.getmro(method.__self__.__class__):
			if method.__name__ in cls.__dict__:
				return cls
		method = getattr(method, '__func__', method)  # fallback to __qualname__ parsing
	if inspect.isfunction(method):
		cls = getattr(inspect.getmodule(method),
					  method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
					  None)
		if isinstance(cls, type):
			return cls
	return getattr(method, '__objclass__', None)  # handle special descriptor objects

def make_method_hookable(method):
	cls = get_defining_class(method)
	def triggering_method(*args):
		cleaned_name = method.__name__.replace('__', '')
		overwritten_args = cls.trigger(cleaned_name, args, args)
		if overwritten_args is not None:
			args = overwritten_args
		return method(*args)
	setattr(cls, method.__name__, triggering_method)