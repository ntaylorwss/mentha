from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="scraper",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.10,<3.11",
    install_requires=install_requires,
    include_package_data=True,
)
