"""Package setup"""
import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

requirements = ["click", "rich<=7.1.0", "simple-term-menu", "requests"]

# Development Requirements
requirements_dev = [
    "pytest<=4.*",
    "black<=20.8b1",
    "pre-commit",
    "mypy",
]

setuptools.setup(
    name="air-quality-cli",
    version="0.0.3",
    author="Yankee Maharjan",
    url="https://github.com/yankeexe/air-quality-cli",
    description="Get Air Quality Index from your CLI",
    license="MIT",
    packages=setuptools.find_packages(
        exclude=["dist", "build", "*.egg-info", "tests"]
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    entry_points={"console_scripts": ["air = air_quality_cli.app:cli"]},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
)
