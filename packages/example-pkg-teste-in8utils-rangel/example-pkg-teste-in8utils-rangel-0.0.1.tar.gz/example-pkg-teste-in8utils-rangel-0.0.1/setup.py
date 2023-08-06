import os
from setuptools import find_packages, setup
from dotenv import load_dotenv

load_dotenv()

with open("README.md", "r") as f:
    long_description = f.read()

current_version = os.getenv('VERSION').split('.')

new_version: list = current_version.copy()
new_version[-1] = str((int(new_version[-1]) + 1))
new_version_str = '.'.join(new_version)

setup(
    name="example-pkg-teste-in8utils-rangel", # Replace with your own username
    version="0.0.1",
    author="Marcelo Rangel",
    author_email="marcelojrrangel@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),   
    install_requires=[
        "bleach==3.1.0",
        "certifi==2019.9.11",
        "chardet==3.0.4",
        "docutils==0.15.2",
        "idna==2.8",
        "mysqlclient==1.4.6",
        "pkginfo==1.5.0.1",
        "Pygments==2.4.2",
        "PyMySQL==0.9.3",
        "python-dotenv==0.10.3",
        "readme-renderer==24.0",
        "requests==2.22.0",
        "requests-toolbelt==0.9.1",
        "sentry-sdk==0.12.3",
        "six==1.12.0",
        "SQLAlchemy==1.3.13",
        "tqdm==4.36.1",
        "twine==2.0.0",
        "urllib3==1.25.6",
        "webencodings==0.5.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)

with open('./.env', 'w') as f:
    f.write(f"VERSION={new_version_str}")
