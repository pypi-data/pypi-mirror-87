import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xdagtool", # Replace with your own username
    version="0.2",
    author="Larry Wu",
    author_email="rulerson@qq.com",
    description="Xdag slicing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['python-dateutil', 'click'],
    keywords='xdag',
    entry_points = {
        'console_scripts': ['xdag-slice=xdagtool.xdu:cmd_go'],
    },
)
