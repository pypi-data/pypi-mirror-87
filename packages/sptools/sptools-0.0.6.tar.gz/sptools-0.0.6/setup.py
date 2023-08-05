import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sptools", # Replace with your own username
    version="0.0.6",
    author="jwh",
    author_email="18981453250@163.com",
    description="test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/jwh-wowo/ceshi.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)