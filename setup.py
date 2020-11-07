import setuptools

setuptools.setup(
    name='rpi_animations',
    version='0.0.1',
    packages=setuptools.find_packages(include=['rpi_animations']),
    url='https://github.com/Anski-D/rpi_animations',
    license='MIT',
    author='David Anscombe',
    author_email='dave.anski@gmail.com',
    description='Text animations for custom messages.',
    python_requires='>=3.7',
    install_requires=['pygame']
)
