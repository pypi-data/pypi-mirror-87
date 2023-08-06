import re

import setuptools

with open("rak_tools/__init__.py", "r") as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rak_ui",  # Replace with your own username
    version=version,
    author="marvinYu",
    author_email="marvin_ywf@163.com",
    description="UI package for lightras tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "wxPython>=4.1.0",
    ],
    python_requires='>=3.6',
)
