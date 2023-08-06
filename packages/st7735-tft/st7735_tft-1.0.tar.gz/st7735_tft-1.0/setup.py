import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="st7735_tft",
    version="1.0",
    author="Frederic",
    description="Python library for controlling ST7735 based displays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Frederic98/st7735_tft",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
