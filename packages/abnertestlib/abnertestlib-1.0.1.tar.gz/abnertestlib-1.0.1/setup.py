# from distutils.core import setup
from setuptools import setup

def readme_file():
      with open("README.rst", encoding="utf-8") as rf:
            return rf.read()

setup(name="abnertestlib", version="1.0.1", description="this is a niubi lib",
      packages=["abnertestlib"], py_modules=["Tool"], author="ABNER", author_email="924770619@qq.com",
      long_description=readme_file(), url="https://github.com", license="MIT")

