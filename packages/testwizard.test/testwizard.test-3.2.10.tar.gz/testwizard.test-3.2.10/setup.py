from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="testwizard.test",
    version="3.2.10",
    author="Eurofins Digital Testing - Belgium",
    author_email="support-be@eurofins.com",
    description="Testwizard test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    install_requires=[
          'testwizard.core==3.2.10',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)





