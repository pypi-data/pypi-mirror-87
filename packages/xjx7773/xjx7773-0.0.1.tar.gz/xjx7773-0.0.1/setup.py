import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "xjx7773",
    version = "0.0.1",
    author = "xjx this is me",
    author_email = "jixuanxu@163.com",
    description = "try to put on pip to install",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/XJX777",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
