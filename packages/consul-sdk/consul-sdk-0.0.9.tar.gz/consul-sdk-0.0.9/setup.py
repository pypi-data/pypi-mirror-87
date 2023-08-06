import setuptools

setuptools.setup(
    name="consul-sdk",
    version="0.0.9",
    author="Noob Dev",
    author_email="author@example.com",
    description="Interface for consul",
    long_description="This is a very long description, like very wrong.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    extras_require={"test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8"]},
)
