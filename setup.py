from setuptools import setup

setup(
    name='pwapi',
    packages=['pwapi'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy'
    ],
)
