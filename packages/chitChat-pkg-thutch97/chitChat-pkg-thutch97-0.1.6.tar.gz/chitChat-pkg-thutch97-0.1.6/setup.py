import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='chitChat-pkg-thutch97',
      version='0.1.6',
      author='Tom Hutchinson',
      author_email='thomas.3.hutchinson@bt.com',
      description='A python chat server client package.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires = [
		'requests==2.24.0'
      ],
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6'
     )