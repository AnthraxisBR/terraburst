from setuptools import setup

setup(
    name="terraburst",
    version="0.1",
    packages=["terraburst"],
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "terraburst=terraburst.cli:cli",
        ],
    },
)
