from setuptools import find_packages, setup
setup(
    name='formatlib',
    packages=find_packages(),
    version='0.1.0',
    description='Format JSON data - location and date  -> DE Standards',
    author='GuyDE',
    license='MIT',
    test_suite='tests',
    url='https://github.com/guylandoy/format-lib',
    install_requires=['pyproj', 'python-benedict'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],

)

