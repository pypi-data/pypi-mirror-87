from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='helloworld-ashcoder',
    version='0.0.1',
    description='Say hello!',
    py_modules=["helloworld"],
    package_dir={'':'src'},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_descrioption_content_type="text/markdown",
    install_requires=[
        "blessings~=1.7",
    ],
    extras_require={
        "dev":[
            "pytest >= 3.7",
            "check-manifest",
            "twine",
        ],
    },
    url="https://github.com/card4ash/pythonpackaging",
    author="Ashraful Alam",
    author_email="card4ash@live.com"
)