import setuptools


INSTALL_REQUIRES = [
    'numpy',
    'sympy',
    'des',
    'pycryptodome'
]


setuptools.setup(
    name="cns_algos", 
    version="0.0.1",
    author="Charles Samuel R",
    author_email="rcharles.samuel99@gmail.com",
    description="A package with all algorithms used in Cryptography. Detailed list in README.",
    url="https://github.com/charlescsr/cns_algos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=INSTALL_REQUIRES,
    zip_safe=False
)