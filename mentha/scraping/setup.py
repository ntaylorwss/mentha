from setuptools import find_namespace_packages, setup

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="mentha-scraping",
    packages=find_namespace_packages(include=["mentha.*"]),
    python_requires=">=3.10,<3.11",
    package_data={
        "scraping": ["py.typed"],
    },
    install_requires=install_requires,
)
