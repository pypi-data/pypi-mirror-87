import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nauts_ml_envs", # Replace with your own username
    version="0.0.1.40",
    author="Richard Hamilton",
    author_email="richard.ha@mathstronauts.ca",
    description="Python library of environments to facilitate practicing machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mathstronauts/mathstropy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=[
          'pygame',
          'matplotlib',
		  'mathstropy'
      ],
    python_requires='>=3.6',
)
