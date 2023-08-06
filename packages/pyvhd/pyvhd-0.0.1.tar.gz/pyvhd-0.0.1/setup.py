import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvhd",
    version="0.0.1",
    author="Ian McLeod",
    author_email="imcleod@redhat.com",
    description="Pure python code to create dynamic VHD files for Xen/Xenserver imports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lungj/pyvhd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)