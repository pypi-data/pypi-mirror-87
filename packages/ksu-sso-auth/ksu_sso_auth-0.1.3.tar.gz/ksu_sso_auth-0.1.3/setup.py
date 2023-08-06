import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ksu_sso_auth",  # Replace with your own username
	version="0.1.3",
	author="Dmitry Shoytov",
	author_email="shoytov@gmail.com",
	description="Module for use ksu sso service ",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/shoytov/sso_auth",
	packages=setuptools.find_packages(),
	package_data={'sso_auth.templates': '*', 'sso_auth.static': '*'},
	install_requires=[
		'requests',
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
