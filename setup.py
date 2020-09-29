from setuptools import find_packages, setup
setup(
    name='formatlib',
    packages=find_packages(include=['formatter']),
    version='0.1.0',
    description='Format JSON data',
    author='GuyDE',
    license='MIT',
    test_suite='tests',
)
