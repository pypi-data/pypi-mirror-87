import setuptools
from pathlib import Path
setuptools.setup(name="hemantadon",
                 version=1.0,
                 packages=setuptools.find_packages(exclude=["data", "tests"]),
                 long_description=Path("README.md").read_text()
                 )
