import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
print(setuptools.find_packages())

setuptools.setup(
    name="yeswehack",
    version="0.6.3",
    author="Jean Lou Hau",
    author_email="jl.hau@yeswehack.com",
    description="YesWeHack API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://yeswehack.com",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite="yeswehack.tests.api_test",
)
