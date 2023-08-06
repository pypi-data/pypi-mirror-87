import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='pyraider',
    version='1.0.8',
    packages=setuptools.find_packages(),    
    author='Tilak Thimmappa',
    author_email='tilaknayarmelpal@gmail.com',
    description="Using PyRaider You can scan installed dependencies known security vulnerabilities. It uses publicly known exploits, vulnerabilities database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points ={ 
        'console_scripts': [ 
            'pyraider = pyraider.cli:main'
        ] 
    }, 
    url="https://github.com/raidersource/pyraider",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    keywords = ['SCA', 'pyraider', 'Source Composition Analysis', 'vulnerability scanner'],   # Keywords that define your package best
    install_requires=[
        'docopt',
        'beautifultable',
        'colored',
        'json2html'
    ],
)