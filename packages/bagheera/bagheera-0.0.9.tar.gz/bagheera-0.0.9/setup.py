import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bagheera", # Replace with your own username
    version="0.0.9",
    author="Bagheera",
    author_email="bergmann.jerome@gmail.com",
    description="An implementation of the bagheera programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bagheera-lang/bagheera-python",
    install_requires=[
        'pyparsing',
    ],
    entry_points={
        'console_scripts': [
            'bagheera=bagheera.cli:main'
        ]
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)