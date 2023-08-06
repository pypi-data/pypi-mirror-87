import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qsync_control",
    version="2.0.1",
    author="Tao Xie",
    author_email="taoxie@alumni.unc.edu",
    description="Python library for operating QMotion blinds controlled a QSync device.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exitexit/qsync-control",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
