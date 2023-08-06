import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graphbar",
    version="0.0.2",
    author="Manuel Gil",
    author_email="manuelgilsitio@gmail.com",
    description="Make bar graph by groups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuelgilm/graphbar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


