import setuptools

with open("README.md", "r") as file_handler:
    long_description = file_handler.read()

setuptools.setup(
    name="hxid",
    version="0.1.1",
    author="Peter Morgan, HomeX LLC",
    author_email="pmorgan@homex.com",
    description="A package to generate and validate HomeX ID's (HXID's)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HomeXLabs/hxid-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

