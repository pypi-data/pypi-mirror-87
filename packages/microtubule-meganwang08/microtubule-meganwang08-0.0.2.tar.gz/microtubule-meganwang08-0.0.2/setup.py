import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="microtubule-meganwang08", # Replace with your own username
    version="0.0.2",
    author="Megan Wang",
    author_email="yinghan@caltech.edu",
    description="microtubule catastrophe Bebi103a package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meganwang08/micotubule",
    packages=setuptools.find_packages(),
    install_requires=["numpy","pandas", "bokeh>=1.4.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
