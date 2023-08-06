import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skltools", # Replace with your own username
    version="0.0.1",
    author="zuel_quant_tools",
    author_email="18981453250@163.com",
    description="for scikit-learn package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/znuel_quant/skltools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)