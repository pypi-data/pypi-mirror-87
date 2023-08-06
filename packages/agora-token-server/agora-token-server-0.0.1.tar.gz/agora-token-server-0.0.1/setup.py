import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "agora-token-server",
    version = "0.0.1",
    author = "Sai Sandeep Rayanuthala",
    author_email = "rayanuthalas@gmail.com",
    description = "Agora Token Server",
    entry_points = {"console_scripts" : [
                        'token_server = token_server:cli'
        ]},
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires = '>=3.6',
    
)