from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=1.1.4", "beautifulsoup4>=4.9.3", "XlsxWriter>=1.3.7"]

setup(
    name="sbireport",
    version="0.0.2",
    author="shurajan",
    author_email="neverbreaks2020@gmail.com",
    description="A package to parse Sberbank Investor html reports",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/neverbreaks/sbi-report",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
