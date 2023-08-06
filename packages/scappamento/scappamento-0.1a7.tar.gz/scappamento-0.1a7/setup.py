import setuptools

from scappamento.__about__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.readlines()


# TODO: read requirements from file (skip setuptools etc.)

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
    install_requires=requirements,
    python_requires='>=3.6'
)
