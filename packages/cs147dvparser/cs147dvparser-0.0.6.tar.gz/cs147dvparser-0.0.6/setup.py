import setuptools

with open("Python/README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cs147dvparser",
    version="0.0.6",
    author="Richard DeAmicis, Jordan Conragan",
    author_email="rtdeamicis@gmail.com, jordanvonpordan@gmail.com",
    description="converts CS147DV assembly language instructions into hexadecimal code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://rdeamici.github.io/CS147DVParser/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Java",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls = {
        'Source': 'https://github.com/rdeamici/CS147DVParser/tree/master/CS147DVPyParser',
        
    }
)