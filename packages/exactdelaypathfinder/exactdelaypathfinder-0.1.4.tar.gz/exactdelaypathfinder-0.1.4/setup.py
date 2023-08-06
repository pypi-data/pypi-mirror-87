from setuptools import find_packages, setup

setup(
    name='exactdelaypathfinder',
    packages=find_packages(include=['exactdelaypathfinder']),
    version='0.1.4',
    description='Obtain paths with total delays equal or close to the user\'s requirements.',
    author='Jessela Baniqued, Daniel Bruce, Daniel Manso, Zachary Quevedo, Marvin Torres',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)