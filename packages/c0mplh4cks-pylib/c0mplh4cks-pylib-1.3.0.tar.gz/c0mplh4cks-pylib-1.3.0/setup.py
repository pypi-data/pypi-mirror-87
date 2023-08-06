from setuptools import setup, find_packages



README = open("README.md").read()



setup(  name = "c0mplh4cks-pylib",
        version = "1.3.0",
        description = "c0mplh4cks's custom library's including Screem and Packnet",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/c0mplh4cks/python3-library",
        author = "c0mplh4cks",
        license = "MIT",
        packages = find_packages(),
        python_requires = ">=3",
)
