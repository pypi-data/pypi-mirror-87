import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="busie-flask-helper",
    version="2.2.1",
    author="Brady Perry",
    author_email="brady@getbusie.com",
    description="A helper for abstracting boilerplate Flask initialization code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bradyperry@bitbucket.org/busie/busie-db-helper.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_migrate',
        'sqlalchemy_utils',
        'redis',
        'python-jose',
        'authlib',
        'requests'
    ]
)
