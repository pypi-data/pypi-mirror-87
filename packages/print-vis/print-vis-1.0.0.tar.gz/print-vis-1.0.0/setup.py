from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="print-vis",
    version="1.0.0",
    description="A lightweight python module to visualize progress and other tasks to boost your console window",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ProgrammingNerdGit/print_vis",
    author="Gavin Distaso",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=["print_vis"],
    include_package_data=True,
    install_requires=["threading","time"]
)