import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AdEncoding", # Replace with your own username
    version="2",
    author="CraftYun83",
    author_email="craftyun83@gmail.com",
    description="The most advanced yet simplest encoding system!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CraftYun83/AVEncoding",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)