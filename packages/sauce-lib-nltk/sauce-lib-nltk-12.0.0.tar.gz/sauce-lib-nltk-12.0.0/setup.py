import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sauce-lib-nltk",
    version="12.0.0",
    author="William Greenly",
    author_email="wmg@dneg.com",
    description="gets synonyms and hypernyms of labels for an asset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    tests_require=['unittest'],
    test_suite="test",
    packages=setuptools.find_packages(),
    include_package_data = True,
    install_requires=[
        'nltk','rdflib','rdflib-jsonld','requests','twine', 'inflect'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)