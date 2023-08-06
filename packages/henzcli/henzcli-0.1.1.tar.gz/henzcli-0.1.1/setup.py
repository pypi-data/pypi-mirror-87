import setuptools 
setuptools.setup(
    name = 'henzcli',
    version = '0.1.1',
    author="Henry Zerocool",
    author_email="phnguyen7@myseneca.ca",
    description="CLI tool to check healthy links",
    url="https://github.com/HenryZerocool/henzcli",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests == 2.24.0",
        "beautifulsoup4 == 4.9.1",
        "datetime == 4.3",
        "colorama == 0.4.4",
        "black == 20.8b1",
        "flake8 == 3.8.4",
        "pytest == 6.1.2",
        "pytest-cov == 2.10.1",
    ],
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'henzcli = main:main'
        ]
    },
    python_requires=">=3.6",
)
