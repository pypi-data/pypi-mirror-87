import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alphorder",  # Replace with your own username
    version="0.1.0",
    author="riolp9991",
    author_email="riolp9991@gmail.com",
    description="Sort a folder's content with just one line of code",
    long_description=open('README.md').read(),
    license="MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/riolp9991/alphorder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "alphorder = alphorder.__main__:main"
        ]
    },
    python_requires='>=3.6',
)
