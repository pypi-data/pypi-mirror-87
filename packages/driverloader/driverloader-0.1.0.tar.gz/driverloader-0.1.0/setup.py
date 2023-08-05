import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="driverloader", # Replace with your own username
    version="0.1.0",
    author="Looker W.",
    author_email="looker53@sina.com",
    description="A browser webdriver downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/looker53/webdriver-downloader",
    packages=['driverloader'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'driverloader=driverloader.cli:cli',
        ],
    },
)