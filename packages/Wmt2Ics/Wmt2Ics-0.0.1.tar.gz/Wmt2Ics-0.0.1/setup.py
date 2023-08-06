import setuptools

with open("README.md", 'r') as f:
	long_description = f.read()

setuptools.setup(
	name = "Wmt2Ics",
	version = "0.0.1", # change before updating
	author = "M. Holbert Roberts",
	author_email = "mhr320@gmail.com",
	description = "Converts wmt schedule Views:My Schedule to .ics file",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/mhr320/Wmt2Ics",
	packages = setuptools.find_packages(),
	package_data={'wmt2ics': ['shift_cats.data','wmtconfig.json'],},
	install_requires=['icalendar','validate_email'],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires = '>=3.8'
	)