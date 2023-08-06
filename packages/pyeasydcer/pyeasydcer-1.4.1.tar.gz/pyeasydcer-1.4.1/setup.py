import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyeasydcer",
    version="1.4.1",
    description="Easy way to import default content in Drupal 8 using python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ruthvikvegunta/pyeasydcer/",
    author="Ruthvik Vegunta",
    author_email="ruthvikv@icloud.com, ruthvikvegunta2@gmail.com",
    keywords=["Drupal", "Default Content", "dcer", "easydcer"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    entry_points = {
         "console_scripts": ['pyeasydcer = easydcer.easydcer:main']
     },
)