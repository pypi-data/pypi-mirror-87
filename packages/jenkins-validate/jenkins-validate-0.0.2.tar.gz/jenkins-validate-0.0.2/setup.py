import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jenkins-validate", # Replace with your own username
    version="0.0.2",
    author="emmawang",
    author_email="xuenwang@ebay.com",
    description="An auto validate package about jenkins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.corp.ebay.com/UFES-dev/ufes-tess-validator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
