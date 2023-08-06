from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "numpy==1.19.3",
    "yfinance>=0.1.55",
    "pandas==1.1.4",
    "apimoex>=1.2.0",
    "scikit-learn>=0.23.2",
    "tqdm>=4.53.0",
]

setup(
    name="pfo",
    version="0.0.6",
    author="shurajan",
    author_email="neverbreaks2020@gmail.com",
    description="A package to analyse personal investments",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/neverbreaks/pfo",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
