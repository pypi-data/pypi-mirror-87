from setuptools import setup, find_packages


setup(
    name="klogs",
    version="2.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    license="Not Open Source",
    install_requires=[
        "click>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "klogs = klogs.cli:main",
        ]
    },
)
