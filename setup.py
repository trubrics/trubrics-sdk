import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlting-jk",
    version="0.0.1",
    author="Jeff Kayne",
    author_email="jeffkayne94@gmail.com",
    description="Mlting package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "mlting"},
    packages=setuptools.find_packages(where="mlting"),
    python_requires=">=3.6",
)
