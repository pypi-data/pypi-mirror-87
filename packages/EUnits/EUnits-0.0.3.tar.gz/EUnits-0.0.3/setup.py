import setuptools

with open("README.org", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EUnits",
    version="0.0.3",
    author="Ethan Sunshine",
    description="A simple units package",
    long_description='This python package adds a single class, the Quantity. It is meant to help you keep track of units when doing physical/scientific/engineering calculations. For more information please visit https://github.com/ethansun01/EUnits',
    url="https://github.com/ethansun01/EUnits",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

print('setup.py running!')
