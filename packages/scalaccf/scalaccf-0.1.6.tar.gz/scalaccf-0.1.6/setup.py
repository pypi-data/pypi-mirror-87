from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="scalaccf",
    packages=["scalaccf"],
    entry_points={
        "console_scripts": ['scalaccf = scalaccf.ScalaCCF:main']
    },
    version='0.1.6',
    description="ScalaCCF - utility to fix style and documentation comments in Scala files",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Taisiia Velychko",
    author_email="justataya@gmail.com",
    url="https://github.com/JustTaya/MetaProg/tree/lab-2/Lab2",
)