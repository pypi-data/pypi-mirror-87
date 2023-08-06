import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="certora-cli-beta",
    version="1.0.13",
    author="Certora",
    author_email="support@certora.com",
    description="Utilities for building smart contracts for verification using the Certora Prover, and for running the Certora Prover",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Certora/CertoraCLI",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "tabulate", "requests", "pycryptodome", "tqdm", "click"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "certoraRun = certora_cli.certoraRun:main",
            "certoraBuild = certora_cli.certoraBuild:main"
        ]
    },
    python_requires='>=3.5',
)
