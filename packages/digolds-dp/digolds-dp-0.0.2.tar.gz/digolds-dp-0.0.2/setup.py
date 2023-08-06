import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="digolds-dp",
    version="0.0.2",
    author="SLZ",
    author_email="founders@digolds.cn",
    description="An easy-to-use data pipeline for data analysts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/digolds/dp",
    entry_points={
        'console_scripts': [
            'dp = dp:run',
        ],
    },
    packages=setuptools.find_packages(),
    # https://python-packaging.readthedocs.io/en/latest/dependencies.html
    install_requires=[
        'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)