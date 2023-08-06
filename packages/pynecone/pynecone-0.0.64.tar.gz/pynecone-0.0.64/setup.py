import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pynecone",
    version="0.0.64",
    description="Build your CLI with ease",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/markolaban/pynecone",
    author="Marko Laban",
    author_email="marko.laban@l33tsystems.com",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    package_data={'': ['*.jinja']},
    include_package_data=True,
    install_requires=["requests==2.23.0",
                      "requests_toolbelt==0.9.1",
                      "python-dotenv",
                      "keyring",
                      "tabulate",
                      "pika",
                      "pykka",
                      "SQLAlchemy",
                      "Jinja2",
                      "pyyaml",
                      "certifi",
                      "flask==1.1.2",
                      "flask-mqtt"],
    entry_points={
        "console_scripts": [
            "pynecone=pynecone.__main__:main",
        ]
    },
)
