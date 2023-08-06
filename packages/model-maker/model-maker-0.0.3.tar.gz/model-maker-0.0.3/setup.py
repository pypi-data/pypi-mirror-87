from distutils.core import setup
from setuptools import find_packages
from modelmaker import __version__

setup(
    name='model-maker',
    version=__version__,
    author='shirecoding',
    author_email="shirecoding@gmail.com",
    scripts=['bin/modelmaker'],
    install_requires=[
        'Jinja2',
        'opencv-python',
        'numpy'
    ],
    url='https://github.com/shirecoding/ModelMaker',
    download_url='https://github.com/shirecoding/ModelMaker/archive/0.0.2.tar.gz',
    long_description=open('README.md').read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    packages=find_packages() + [
        'modelmaker.resources'
    ],
    package_data={
        'modelmaker.resources': [
            'templates/*',
            'templates/**/*',
            'templates/**/**/*',
            'templates/**/**/**/*',
            'templates/**/**/**/**/*',
        ]
    }
)