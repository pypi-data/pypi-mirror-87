import setuptools
from pathlib import Path
setuptools.setup(
name="jjspython",
version="1.0",
long_description=Path("README.md").read_text())
setuptools.find_packages(exclude=["tests","data"])

