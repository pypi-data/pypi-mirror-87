import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tpfunc", # Replace with your own username
    version="1.0.0",
    author="Justin Tung",
    author_email="justincp.tung@moxa.com",
    description="ThingsPro Edge Function SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MOXA-ISD/edge-thingspro-function",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)