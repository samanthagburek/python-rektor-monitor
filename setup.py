from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="my-demo-pack-ex",
    version="0.1.0",
    author="Samantha Gburek",
    author_email="<sgg2056@nyu.edu>",
    description="Monitor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)