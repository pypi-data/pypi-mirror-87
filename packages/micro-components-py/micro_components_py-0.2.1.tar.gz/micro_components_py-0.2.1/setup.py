import os
from setuptools import setup, find_packages

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "micro_components_py",
	version = "0.2.1",
	author = "Dan Borufka",
	author_email = "danborufka@gmail.com",
	description = "Lightweight library to create components that can automagically be used as either CLI or as native classes in other programming languages",
	license = "MIT",
	keywords = "components",
	url = "https://github.com/polygoat/micro-components-py",
	packages=find_packages(),
	install_requires=[
        "pydash",
        "termcolor",
		"colorama",
		"mako"
    ],
    scripts=['micro-components'],
    package_data={
    	'micro_components_py': ['bin/micro-components.py']
    },
	include_package_data=True,
	long_description=read('README.md'),
	long_description_content_type="text/markdown",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Topic :: Utilities",
		"License :: OSI Approved :: MIT License",
	],
)
