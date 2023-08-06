import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name='control_utils',    # This is the name of your PyPI-package.
    version='1.0.4',
    url='https://github.com/ryanGT/control_utils',
    author='Ryan Krauss',
    author_email='ryanwkrauss@gmail.com',
    description="package for helping with teaching or learning feedback control",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
