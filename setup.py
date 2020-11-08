from setuptools import setup, find_packages

setup(
    name='rpi_animations',
    version='0.0.1',
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='https://github.com/Anski-D/rpi_animations',
    license='MIT',
    author='David Anscombe',
    author_email='dave.anski@gmail.com',
    description='Placeholder',
    install_requires=['pygame'],
    package_data={
        'rpi_animations.inputs': ['settings*.json'],
        'rpi_animations.resources': ['*.bmp', '*.svg']
    }
)
