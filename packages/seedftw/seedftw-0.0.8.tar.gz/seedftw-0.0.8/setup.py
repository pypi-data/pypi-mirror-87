import setuptools

setuptools.setup(
    name="seedftw",
    version="0.0.8",
    author="PVF",
    author_email="pvf@dtime.ai",
    description="Simple Energy & Environment Data From The World (aka. seedftw) - A small example package for acquiring open energy and environment data",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Pierre_VF/seedftw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    requires=[
        "casadi",
        "dash",
        "datetime",
        "functools",
        "json",
        "numpy",
        "os",
        "pandas",
        "plotly",
        "pytz",
        "setuptools",
        "urllib",
        "xlrd",
    ],
    install_requires=[
        "casadi",
        "dash",
        "datetime",
        "numpy",
        "pandas",
        "plotly",
        "xlrd",
    ],
)

# More details on how to set this up: https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html
