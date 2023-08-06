import setuptools

try:
  with open("README.md", "r") as fh:
      long_description = fh.read()
except:
	long_description = "A quick and easy way to distribute your python project!"

setuptools.setup(
    name="shipsnake",
    version="0.0.1",
#		scripts=['bin/nought','bin/nt'],
#		entry_points={
#        'console_scripts': ['nought=nought.__main__:main'],
#    },
    author="Cole Wilson",
    author_email="cole@colewilson.xyz",
    description="A quick and easy way to distribute your python project!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cole-wilson/shipsnake",
    packages=setuptools.find_packages(),
		install_requires=['toml'],
    classifiers=["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
		package_data={"": ['*.template'],},
		license="",
		keywords='ship package distribute setuptools snake python',
)