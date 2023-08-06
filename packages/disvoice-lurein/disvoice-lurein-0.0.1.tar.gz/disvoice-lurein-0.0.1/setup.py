import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="disvoice-lurein",
    version="0.0.1",
    author="Lurein Oerera",
    author_email="lureinperera@gmail.com",
    description="A pip installable version of jcvazquezc's DisVoice library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lurein/DisVoice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
