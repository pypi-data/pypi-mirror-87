import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EMFT_LABELS",
    version="0.0.2",
    author="Denis Agafonov",
    author_email="d.a6af0n0v@gmail.com",
    description="Labels layout generator (EMFT)",
    long_description_content_type="text/markdown",
    url="https://github.com/a6af0n0v/emft_labels.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
