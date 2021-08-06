from setuptools import setup, find_packages

setup(
    name='AutoGnirehtet',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    py_modules = [ 'autognirehtet' ],

    install_requires=['pexpect', 'pure-python-adb'],

    entry_points='''
        [console_scripts]
        auto-gnirehtet=AutoGnirehtet.autognirehtet:run
    ''',

    # metadata to display on PyPI
    author='Scott Hamilton',
    author_email='sgn.hamilton+python@protonmail.com',
    description='Automatic reconnect script for gnirehtet',
    keywords='reverse thetering gnirehtet auto reconnect',
    url='https://github.com/SCOTT-HAMILTON/AutoGnirehtet',
    project_urls={
        'Source Code': 'https://github.com/SCOTT-HAMILTON/AutoGnirehtet',
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)
