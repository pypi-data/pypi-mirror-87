import setuptools

with open("README.md", 'r') as f:
    long_desc = f.read()

setuptools.setup(
    name="movefile-restart",
    version="0.6.0",
    author="hammy3502",
    author_email="hammy275@gmail.com",
    description="A small library for Windows to queue files to be moved, deleted, or renamed on reboot.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/hammy3502/python-movefile-restart",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires='>=3.6'
)