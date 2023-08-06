from setuptools import find_packages, setup
setup(
    name='ldkLibrary',
    packages=find_packages(include=['ldkLibrary']),
    version='0.1.1',
    description='My first Python library',
    author='Me',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='test_library',
)