import setuptools

__version__ = '0.0.2'

url = 'https://github.com/jannessm/tensor-observer'

with open("README.md", "r") as fh:
	long_description = fh.read()

def parse_requirements(filename):
	"""Load requirements from a pip requirements file."""
	lineiter = (line.strip() for line in open(filename))
	return [line for line in lineiter if line and not line.startswith("#")]

setuptools.setup(
    name="tensor_observer",
    version=__version__,
    author='Jannes Magnusson',
    author_email="j-magnusson@t-online.de",
    url=url,
    description="A little api library for a TensorObserver server",
	long_description=long_description,
	long_description_content_type="text/markdown",
    license="GNU GPL",
	install_requires=parse_requirements("requirements.txt"),
    packages=["tensor_observer"],
    keywords='tensorObserver tensorflow tensorboard pytorch'
)
