import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sit-calc-rileycworstell",
    version="0.0.1",
    author="Riley Worstell",
    author_email="rcwors02@gmail.com",
    description="Calculate income tax based on state",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rileyworstell/Python-State-Income-Tax",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
