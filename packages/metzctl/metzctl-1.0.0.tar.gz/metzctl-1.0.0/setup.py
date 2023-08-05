import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="metzctl",
    version="1.0.0",
    description="Remote control for Metz televisions",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kaoh/metzctl",
    author="Karsten Ohme",
    author_email="k_o_@users.sourceforge.net",
    license="LGPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["metzctl"],
    include_package_data=True,
    install_requires=["getmac", "wakeonlan"],
    entry_points={
        "console_scripts": [
            "metzctl=metzctl.__main__:main",
        ]
    },
)