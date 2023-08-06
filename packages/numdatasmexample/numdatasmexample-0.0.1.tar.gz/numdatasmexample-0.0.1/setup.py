import setuptools

## all information about project are passed as parameters in setup()
## REFER packaging.python.org

with open("README.md","r") as fh:
	long_description=fh.read()

setuptools.setup(
	name="numdatasmexample",
	version="0.0.1",
	author="Stuti Madaan",
	author_email="abc@xy.com", 
	description="A simple package calculating values for a single number",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="", #github Repo Link
	keywords="package numbers calculations", # how are packagesindexed on pypi,keywords to search package on pypi
	packages=setuptools.find_packages(), # finds packages in current directory by loading init file
	classifiers=[
		"Programming Language :: Python :: 2",
		"Operating System :: OS Independent"
	],
	)


## To build a WHEEL ## 
## python3 -m pip install --user --upgrade setuptools wheel 
## 
## python3 setup.py sdist bdist_wheel

## python3 -m pip install --user --upgrade twine
## 
##python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*



