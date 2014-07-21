import os
from setuptools import setup, find_packages

setup(
    name='grano-images',
    version=os.environ.get('GRANO_RELEASE', '0.3.2'),
    description="An entity and social network tracking software for news applications (Support for images)",
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    keywords='sql graph sna networks journalism ddj entities',
    author='Rizmari Versfeld',
    url='http://docs.grano.cc',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'grano>=0.3.1',
        'Pillow==2.5.1',
    ],
    entry_points={
        'grano.startup': [
            'images = grano.images.base:Installer'
        ]
    },
    tests_require=[]
)
