from setuptools import setup

setup(
	name='htwrapper',
	version='1.1.0',
	author='HedgeTech LLC',
	description='HTClient Official API',
	py_modules=['htwrapper'],
	package_dir={'': 'src'},
	install_requires=['requests >= 2.21.0'],
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6',
)