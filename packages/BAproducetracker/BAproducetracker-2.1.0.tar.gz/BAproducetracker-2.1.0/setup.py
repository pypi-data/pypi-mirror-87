import setuptools
import os
import platform

if platform.system() == 'Windows':

    folder = os.path.dirname(os.path.realpath(__file__))
    req_path = folder + '/requirements.txt'
    install_requires = []

    if os.path.isfile(req_path):
        with open(req_path) as file:
            install_requires = file.read().splitlines()
else:
    folder = os.path.dirname(os.path.realpath(__file__))
    req_path = folder + '/linuxrequirements.txt'
    install_requires = []

    if os.path.isfile(req_path):
        with open(req_path) as file:
            install_requires = file.read().splitlines()

setuptools.setup(
    name="BAproducetracker",
    version="2.1.0",
    author="Brody, Joseph // Dillon, John // Estrada, Pablo",
    url="https://github.com/jd3builds/BadApplesJJP",
    packages=['producetracker'],
    package_data={ 'producetracker': ['*', 'resources/*.png'] },
    include_package_data=False,
    description="Produce expiration tracker",
    python_requires='>=3.8',
    install_requires=install_requires,

    entry_points = {
        'console_scripts': [
            'bapt = producetracker.app:main'
        ]
    }
)
