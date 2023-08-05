import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dltk_ai",
    version="1.1.5",
    author="DLTK",
    author_email="connect@qubitai.tech",
    description="Python Client for DLTK.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dltk-ai/dltk-ai-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
