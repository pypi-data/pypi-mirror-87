from setuptools import setup, find_packages

asteroid_version = "0.3.0"

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="asteroid-filterbanks",
    version=asteroid_version,
    author="Manuel Pariente",
    author_email="manuel.pariente@loria.fr",
    url="https://github.com/asteroid-team/asteroid-filterbanks",
    description="Asteroid's filterbanks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "torch",
    ],
    extras_require={
        "all": ["librosa", "scipy"],
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
