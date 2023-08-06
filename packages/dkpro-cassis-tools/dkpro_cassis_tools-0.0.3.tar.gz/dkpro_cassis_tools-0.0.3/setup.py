import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dkpro_cassis_tools",
    version="0.0.3",
    author="Laurent Bié",
    author_email="l.bie@pangeanic.com  ",
    description="Tools for dkpro cassis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pangeamt/dkpro_cassis_tools",
    packages=setuptools.find_packages(),
    install_requires=[
        'dkpro-cassis>=0.5.0',
        'sequence_transfer>=0.1.0'
    ],
    tests_require=[
        'mecab-python3>=1.0.2',
        'unidic-lite>=1.0.7'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.7',
)
