import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfpa", 
    version="0.0.9",
    author="Erik Warren",
    author_email="erikwarren@yahoo.com",
    description="Leverage the power of Python for corporate finance and accounting functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/warrenpilot/pyfpa",
    packages=setuptools.find_packages('.'),
    install_requires=[
        'pandas >= 1.0.0',
        'numpy >= 1.17',
        'xlrd >= 1.0',
        'openpyxl >= 3.0',
        'pandas_bokeh >= 0.5.2'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Win32 (MS Windows)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business"
    ],
    python_requires='>=3.6',
)