from setuptools import setup, find_packages

with open("README.md", "r") as fread:
    long_description = fread.read()

setup(
    name="dkbirdisland",
    version="0.1.4.dev",
    author="Murilo Castro",
    author_email="murilo.castro@ccc.ufcg.edu.br",
    description="DK, T-rex style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Murilo-Gruppi/DonkeyKong-BirdIsland",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['pygame>=2.0'],
    entry_points={
        'console_scripts': [
            'dkbirdisland = dkbirdisland.__main__:main'
        ]
    }
)

