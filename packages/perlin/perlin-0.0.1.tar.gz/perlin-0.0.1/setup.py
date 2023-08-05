from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="perlin",
    version="0.0.1",
    author="Drake Fletcher",
    maintainer='Drake Fletcher',
    author_email="drakeerv@outlook.com",
    description="A perlin nosie library written in python",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drakeerv/perlin",
    download_url='https://github.com/drakeerv/perlin',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
