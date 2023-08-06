from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'turpy',
    version = '0.0.3',
    description = "tools for python and fun coding",
    packages=['io'],
    py_modules=["turpy","turpy/io/load_yaml"],
    package_dir = {'':'src'},

    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],

    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires = [
        "PyYAML>=5.3.1",
    ],

    extras_require = {
        "dev": [
            "pytest>=6.1.2",
            "twine>=3.2.0",
        ],
    },

    url="https://github.com/drjobel/turpy",
    author="José Beltrán",
    author_email="drjobel.connection@gmail.com",

    maintainer="José Beltrán",
    maintainer_email="drjobel.connection@gmail.com",

)
