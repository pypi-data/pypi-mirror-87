import setuptools
import pathlib
import os
from superwise import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements_path = pathlib.Path(os.path.join("superwise", "requirements.txt"))
with open(requirements_path, "r") as f:
    requirements = [x.strip() for x in f.readlines()]

setuptools.setup(
      name='superwise',
      version=__version__,
      description='Superwise SDK',
      url='https://superwise-doc.readthedocs.io/en/latest/',
      author='Superwise.ai',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author_email="tech@superwise.com",
      license="MIT",
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      packages=setuptools.find_packages(exclude=["tests"]),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=requirements)
