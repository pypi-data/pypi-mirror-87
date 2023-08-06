import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto-pacing", # Replace with your own username
    version="0.0.2",
    author="Michael Aucoin",
    author_email="michael@clicktripz.com",
    description="Utilities designed to automatically set and adjust the pace a time series based on historical trends and specific performance targets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maucoin/auto-pacing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)