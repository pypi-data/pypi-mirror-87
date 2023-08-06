import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GeneralSQL",
    version="0.0.3",
    author="joker-zzp",
    author_email="joker_zzp@qq.com",
    description="From simple to complex SQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joker-zzp/GeneralSQL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.0',
)