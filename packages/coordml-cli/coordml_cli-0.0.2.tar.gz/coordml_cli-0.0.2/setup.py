import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="coordml_cli",
    version="0.0.2",
    author="Yichen Xu",
    author_email="yichen.xu@monad.email",
    description="CLI for CoordML Central",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coordml/cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['requests', 'pyyaml'],
    entry_points={
        'console_scripts': ['cm=coordml_cli.cli:main']
    }
)
