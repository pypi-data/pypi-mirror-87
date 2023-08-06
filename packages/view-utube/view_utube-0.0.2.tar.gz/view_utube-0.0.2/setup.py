from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    url="https://github.com/subrat-lima/view_utube",
    author="Subrat Lima",
    author_email="subrat.k.lima@protonmail.com",
    name='view_utube',
    version='0.0.2',
    description='browse latest videos of your favorite youtube channels from terminal!',
    package_dir={'':'src'},
    packages=find_packages(where='src'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["gazpacho"],
    entry_points={
        'console_scripts': [
            'utube=view_utube:main',
        ],
    },
)
