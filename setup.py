from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='rpi_animations',
    version='0.4.2',
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='https://github.com/Anski-D/rpi_animations',
    license='MIT',
    author='David Anscombe',
    author_email='dave.anski@gmail.com',
    description='Display animated scrolling text and pictures that periodically move.',
    long_description=long_description,
    python_requires='>=3.7',
    install_requires=['pygame<2', 'wheel'],
    package_data={'': ['inputs/*.json', 'inputs/*.bmp']},
    entry_points={
        'console_scripts': [
            'run_rpi_an=rpi_animations:main'
        ]
    }
)
