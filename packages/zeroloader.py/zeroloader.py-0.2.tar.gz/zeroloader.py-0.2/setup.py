import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zeroloader.py",
    version="0.2",
    author="Andrea Wang",
    author_email="ayw255@nyu.edu",
    description="A package to read 0archive's data from google drive to csv",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/disinfoRG/ZeroLoader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["python-dotenv", "google-api-python-client", "google-auth",
                      "google-auth-httplib2", "google-auth-oauthlib", "oauth2client",
                      "pandas"],
    python_requires='>=3.6',
)
