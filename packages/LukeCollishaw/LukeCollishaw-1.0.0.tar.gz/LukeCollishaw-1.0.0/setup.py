import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LukeCollishaw",
    version="1.0.0",
    author="Luke Collishaw-Schepman",
    author_email="lc796@exeter.ac.uk",
    description="COVID Alarm Clock",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lc796/covid-alarm-clock",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)