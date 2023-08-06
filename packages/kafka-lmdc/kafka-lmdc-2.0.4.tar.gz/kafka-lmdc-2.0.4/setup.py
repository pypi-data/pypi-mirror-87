from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

# This call to setup() does all the work
setup(
    name="kafka-lmdc",
    version="2.0.4",
    description="Esta biblioteca tem como objetivo a facilitação do uso de Kerberos e Kafka em Python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/LMDC-UFF/kafka-python",
    author="LMDC-UFF",
    author_email="opensource@lmdc.uff.br",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["kafka_lmdc"],
    include_package_data=True,
    install_requires=["confluent_kafka"],
    entry_points={
        "console_scripts": [
            "kafka-lmdc=kafka_lmdc.demo:main",
        ]
    },
)