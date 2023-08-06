import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="annotated_dataset",
    version="0.0.4",
    author="Laurent Bié",
    author_email="l.bie@pangeanic.com  ",
    description="Annotated dataset analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pangeamt/annotated_dataset",
    packages=setuptools.find_packages(),
    install_requires=[
        'dkpro-cassis>=0.5.0',
        'dkpro-cassis-tools>=0.0.3',
        'networkx>=2.5',
        'pycaprio>=0.2.0',
        'web_anno_tsv>=0.0.1',
        'bokeh>=2.2.3'
    ],
    tests_require=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.7',
)

