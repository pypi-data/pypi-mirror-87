import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfgnlog-YmirSystems",
    version="0.0.2",
    author="Ymir Systems",
    author_email="info@YmirSystems.com",
    description="Simple configuration and log files. Config files use JSON. XDG compliant by default.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YmirSystems/cfgnlog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Artistic License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
)
