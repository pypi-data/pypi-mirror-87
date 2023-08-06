from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nonelib",
    version="0.0.1",
    author="Marc Gurevitx",
    author_email="marcgurevitx@gmail.com",
    description="f(x=None) ≡ f()",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcgurevitx/nonelib",
    py_modules=['nonelib'],
    license="The Unlicense",
)
