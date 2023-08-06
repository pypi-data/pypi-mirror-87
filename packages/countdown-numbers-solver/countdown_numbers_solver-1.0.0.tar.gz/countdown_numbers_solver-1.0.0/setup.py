import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="countdown_numbers_solver",
    version="1.0.0",
    author="Tao Xie",
    author_email="taoxie@alumni.unc.edu",
    description="Python function for solving the numbers game problems in the British game show Countdown.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exitexit/countdown-numbers-solver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
