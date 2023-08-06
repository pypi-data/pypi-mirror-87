from distutils.core import setup
from {{ package_name }} import __version__

setup(
    name='{{ package_name }}',
    version=__version__,
    author='',
    install_requires=[
        'numpy',
        'opencv-python'
    ],
    url='',
    long_description=open('README.md').read(),
    zip_safe=False,
)

