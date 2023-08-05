import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amaptt",
    version="0.0.3",
    author="ewg",
    author_email="essen.wang@outlook.com",
    description="python api for amap travel time calc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iessen/amaptt.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
