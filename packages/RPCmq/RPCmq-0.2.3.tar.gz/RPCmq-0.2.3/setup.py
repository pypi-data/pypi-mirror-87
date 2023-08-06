import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RPCmq",
    version="0.2.3",
    author="nigowl",
    author_email="nigowl@live.com",
    description="Implementation of RPC by message queue call",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pika >= 1.1.0',
    ],
)
