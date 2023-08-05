import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read().replace('```python','').replace('```','')

setuptools.setup(
    name="fimaster",
    version="0.0.0.6",
    author="Gavin Zhang",
    author_email="gavinz0228@gmail.com",
    description="A python library for fixed-income data and valuation.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/gavinz0228/fi-master",
    # packages=setuptools.find_packages("src"),

    packages=['fimaster', 'fimaster.data_api', 'fimaster.valuation'],
    package_dir={
        'fimaster': 'src/fimaster',
        'fimaster.data_api': 'src/fimaster/data_api',
        'fimaster.valuation': 'src/fimaster/valuation',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX'
    ],
    include_package_data=True,
    install_requires=[
        'pandas'
    ]
)