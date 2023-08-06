import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medizinfuchs-mosalam", # Replace with your own username
    version="0.0.1",
    author="Mohamed Hussein(Mo Salam)",
    author_email="mosalam208@gmail.com",
    description="A package to scrap medical products from medizinfuchs.de",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m7salam/medizinfuchs-spider",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ],
    python_requires='>=3.6',
)