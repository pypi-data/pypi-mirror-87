import setuptools

from scappamento.__about__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='scappamento',
    version=__version__,
    author='Lorenzo Bunino',
    author_email="bunino.lorenzo@gmail.com",
    description="B2B automation for music stores",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lorenzobunino/scappamento",
    packages=setuptools.find_packages(),  # TODO: find_packages vs hand-compiled list
    entry_points={
        'console_scripts': [
            'scappamento = scappamento.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",  # TODO: fix path handling and
                                                     #  change "Microsoft :: Windows" to "OS Independent"
    ],
    install_requires=[
        'pandas~=1.1.2',
        'xlrd~=1.2.0',
        'xlutils~=2.0.0',
        'requests~=2.24.0',
        'selenium~=3.141.0',
        'beautifulsoup4~=4.9.3',
        'mysql-connector-python~=8.0.11',
        'chromedriver_binary>=86.0.4240.22.0'
    ],
    python_requires='>=3.6'
)
