import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EarthScan",
    version="0.1",
    author="Benjamin Laken",
    author_email="benjamin@cervest.com",
    description="Pythonic interface to EarthScan.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/Cervest/EarthScan",
    install_requires=['requests>=2.25.0'],
    packages=['EarthScan'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)