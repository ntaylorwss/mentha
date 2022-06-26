from setuptools import find_packages, setup

setup(
    name="mentha-cli",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.10,<3.11",
    include_package_data=True,
    scripts=["bin/mentha", "bin/mentha-image", "bin/mentha-tag", "bin/mentha-build"],
    entry_points={"console_scripts": ["mentha-cli = cli.main:cli"]},
)
