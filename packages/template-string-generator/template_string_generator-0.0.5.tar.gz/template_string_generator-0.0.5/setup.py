import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="template_string_generator",
    version="0.0.5",
    author="Jose Pablo Aramburo",
    author_email="josepablo.aramburo@laziness.rocks",
    description="Generates all possible combinations of a string based on a given template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PootisPenserHere/template_string_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
