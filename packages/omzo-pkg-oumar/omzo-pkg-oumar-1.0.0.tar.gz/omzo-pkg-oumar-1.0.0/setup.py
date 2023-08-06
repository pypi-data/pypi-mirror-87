import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="omzo-pkg-oumar", # Replace with your own username
    version="1.0.0",
    author="Oumar Dia",
    author_email="oumardia8@gmail.com",
    description="Mon premier projet",
    long_description=long_description,
    long_description_content_type=" ",
    url=" ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
