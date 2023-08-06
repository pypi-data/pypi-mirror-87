from setuptools import setup, find_packages
setup(
    name                = 'jh_pypi',

	version             = '0.1',


	description         = 'upload module test',


    author              = 'jh.kim',


	author_email        = 'doorbw@outlook.com',


  url                 = '',


	download_url        = '',


	install_requires    =  [],


    packages            = find_packages(exclude = []),


	keywords            = ['pypi test'],


	python_requires     = '>=3',

	package_data        = {},


	zip_safe            = False,

	classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
