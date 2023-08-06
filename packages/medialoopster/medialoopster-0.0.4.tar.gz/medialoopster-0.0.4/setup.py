import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medialoopster",
    version="0.0.4",
    author="Stéphane Ludwig",
    author_email="gitlab@stephane-ludwig.net",
    description="medialoopster API wrapper for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/medialoopster/medialoopster_python",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
