import setuptools

with open("py_behrtech/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_behrtech",
    version="2020.12.01.1",
    license="MIT",
    author="Matthew Ashley",
    author_email="matthewashley@verntechnologies.com",
    description="A package to interface with BehrTech's gateway API for requesting and parsing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vern-Technologies/py_behrtech",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
