import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pertdist",
    version="0.0.1",
    author="Jason M. Cherry",
    author_email="jcherry@gmail.com",
    description="A scipy-like implementation of the PERT distribution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Calvinxc1/PertDist",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy >=1.17, <2',
        'scipy >=1.3, <2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires='>=3.6',
)