from setuptools import setup

setup(
    name='structured_eligibility',
    packages=['structured_eligibility'],
    include_package_data=True,
    install_requires=[
        'ruamel.yaml',
        'json-logic'
        'flask'
    ],
)
