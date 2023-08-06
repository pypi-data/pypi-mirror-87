from setuptools import setup

def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
        return rf.read()

setup(name="reidpy",
    version="1.0.0",
    description=readme_file(),
    packages=["reidtest"],
    py_modules=["Tool"],
    author="reid",
    author_email="reid21@qq.com",
    long_description="long lib",
    url="https://github.com/rei42",
    license="MIT")
