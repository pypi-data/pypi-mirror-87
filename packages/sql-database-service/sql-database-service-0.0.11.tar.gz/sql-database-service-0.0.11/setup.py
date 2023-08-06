import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sql-database-service",
    version="0.0.11",
    author="Quaking Aspen",
    author_email="info@quakingaspen.net",
    license='MIT',
    description="This repo provides a library to do the basic CRUD operations in addition to grouping and sorting on an SQL database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quakingaspen-codehub/sql_database_service",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platform=['Any'],
    python_requires='>=3.6',
)