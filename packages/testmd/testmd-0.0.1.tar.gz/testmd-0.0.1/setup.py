import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testmd",
    version="0.0.1",
    author="Mark Sellors",
    author_email="python@5vcc.com",
    description="A simple tool to test markdown front matter yaml",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sellorm/mdtest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['bin/testmdcli'],
    install_requires=[
          'python-frontmatter>=0.5.0',
      ],
)
