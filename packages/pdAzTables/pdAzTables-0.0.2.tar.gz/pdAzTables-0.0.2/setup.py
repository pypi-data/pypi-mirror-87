from setuptools import find_packages, setup

classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
]

setup(
    name='pdAzTables',
    packages=find_packages(),
    version='0.0.2',
    download_url='https://github.com/Gorgoras/PandasAzureTables/archive/v0.0.2.tar.gz',
    description='Easy Azure table storage into Pandas dataframe',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    author='Martin Zurita',
    author_email='martinzurita1@gmail.com',
    license='MIT',
    classifiers=classifiers,
    install_requires=[
        'azure-cosmosdb-table', 
        'pandas'
    ],
    keywords=['Pandas', 'Azure', 'NoSQL', 'Data']
)
