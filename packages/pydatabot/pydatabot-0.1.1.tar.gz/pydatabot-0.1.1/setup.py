import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pydatabot',  
    version='0.1.1',
    #scripts=['pydevbot'],
    author="Xin SUN",
    author_email="ethan.sun921107@gmail.com",
    description="Bot for DS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XIN-von-SUN",

    packages=setuptools.find_packages(),
    include_package_data=True,
    
    install_requires=['dialogflow', 'pandas', 'numpy'],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ]
 )