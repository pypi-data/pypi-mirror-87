import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdt4160",
    version="1.1.1",
    author="Fisherman's Friend",
    author_email="fish@waifu.club",
    description="Easy simulations for lower level tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitgud.io/fish/tdt4160",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"
)
