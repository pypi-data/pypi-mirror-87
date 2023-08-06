import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="firebaseHelper",
    version="0.0.1",
    author="Luis Zepeda",
    author_email="luiszepedavarela@comunidad.unam.mx",
    description="Firebase helper (fork from pyrebase)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luis-zepeda/firebaseHelper.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['oauth2client', 'requests']
)