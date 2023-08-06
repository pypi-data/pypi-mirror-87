import os
import re
import sys
import unittest

sys.path.insert(0, os.getcwd())

from utils.shell import shell_run
from utils.classes.Component import Component

class TestComponentClass(unittest.TestCase):
	def test_instantiation(self):
		print(' Testing Component class instantiation ...')
		from components import Builder
		assert callable(Builder.create)
		
	def test_help_helper(self):
		print(' Testing help helper ...')
		result = shell_run(['./components/builder.py', 'help'])

		assert re.search('Available methods', result) is not None
		assert re.search('Available properties', result) is not None
		assert re.search('.create', result) is not None
		assert re.search('component_name', result) is not None
		assert re.search('.engine', result) is not None
		
	def test_method_help_helper(self):
		print(' Testing method helper ...')
		result = shell_run(['./components/builder.py', 'create', '--help'])

		assert re.search('positional arguments:', result)
		assert re.search('component_name_pos', result)
		assert re.search('optional arguments:', result)
		assert re.search(r'--component_name \[COMPONENT_NAME\]', result)


class TestComponentInteraction(unittest.TestCase):
	def test_python_and_node(self):
		print(' Testing interaction between Python and Node components ...')
		result = shell_run(['micro-components', 'create', 'receiver', 'python'])
		
		with open('./receiver.py', 'r') as py_file:
			py_lines = py_file.read().split('\n')

		with open('./broker.sh', 'w') as sh_file:
			sh_file.write("""#!/bin/sh\n\necho '{ "hello": "world" }'""")
		os.chmod('./broker.sh', 0o775)

		py_lines[2] = py_lines[2].replace('micro_components', 'utils.classes.Component')
		py_lines.insert(3, "Broker = Component.from_cli('./broker.sh')")
		py_lines.insert(11, "\tdef run(key):\n\t\treturn Broker.anything()[key]")

		with open('./receiver.py', 'w') as py_file:
			py_file.write('\n'.join(py_lines))

		result = shell_run(['./receiver.py', 'run', 'hello'])
		assert result == "world"

		os.remove('./receiver.py')
		os.remove('./broker.sh')

class TestComponentBuilder(unittest.TestCase):
	def test_component_creation(self):
		print(' Testing creation of components via CLI ...')
		result = shell_run(['micro-components', 'create', '--color=false', "My Component", 'python']);
		assert result == 'Component created. Try it by running ./my_component.py help'

		with open('./my_component.py', 'r') as component_file:
			content = component_file.read()

		with open('./my_component.py', 'w') as component_file:
			content = content.replace(' micro_components ', ' utils.classes.Component ')
			component_file.write(content)

		from my_component import MyComponent

		assert MyComponent.is_component
		assert MyComponent.name == 'my_component'

		os.remove('./my_component.py')

if __name__ == '__main__':
	unittest.main()