import setuptools

setuptools.setup(
    name='DiscoverPagination',
    version='0.1.0',
    packages=setuptools.find_packages(),
    license='MIT',
    author_email="dhking@wharton.upenn.edu",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=['fuzzywuzzy', 'python-Levenshtein'],
)