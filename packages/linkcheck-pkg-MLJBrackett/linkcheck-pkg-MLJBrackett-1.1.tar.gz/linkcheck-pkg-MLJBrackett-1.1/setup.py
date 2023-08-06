import setuptools

with open("docs/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linkcheck-pkg-MLJBrackett",  # Replace with your own username
    version="1.1",
    author="Michael Brackett",
    author_email="mljbrackett@gmail.com",
    description="A simple link checking program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MLJBrackett/link-check",
    license="MIT",
    install_requires=[
        "requests",
        "argparse",
        "colorama",
        "black",
        "flake8",
        "coverage",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "link_check = src.link_check:main_wrapper",
        ]
    },
    python_requires=">=3.8",
)
