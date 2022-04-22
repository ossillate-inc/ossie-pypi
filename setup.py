from setuptools import setup, find_packages

import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# this grabs the requirements from requirements.txt
#REQUIREMENTS = [i.strip() for i in open(os.path.join(here, "requirements.txt")).readlines()]

setup(
	name = 'ossie',
	packages=find_packages(),
	package_data={'ossie': ['config.ini']},
	version = '0.2',
	license='MIT',
	description = 'Ossie is a smart assistant that alerts developers of "risky" Python PyPi packages in their software supply chain',
    long_description=long_description,
    long_description_content_type="text/markdown",
	author = 'Ossillate Inc.',
	author_email = 'oss@ossillate.com',
	url = 'https://github.com/ossillate-inc/ossie-pypi',
	download_url = 'https://github.com/ossillate-inc/ossie-pypi/archive/refs/tags/placeholder.tar.gz',
    project_urls={
        "Bug Tracker": "https://github.com/ossillate-inc/ossie-pypi/issues",
    },
	keywords = ['software supply chain attacks', 'typo-squatting', 'python', 'open-source software', 'software composition analysis'],
	python_requires=">=3.4",
	install_requires=[
		'requests',
		'python_dateutil',
		'pyyaml',
		'requests',
		'configparser',
		'pipreqs',
	],
	entry_points = {
		'console_scripts': [
			'ossie=ossie.__main__:main',
			'ossie-pip=ossie.pip:main'
		],
	},
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)
