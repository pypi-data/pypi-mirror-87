import setuptools

with open("README.md", "r") as filehandler:
	long_description = filehandler.read()

setuptools.setup(
	name = "mattia80511",
	version = "0.1",
	author_email = "mattai0311@gmail.com",
	description = "A personal utility package.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
	],
	python_requires='>=3.6',
)
