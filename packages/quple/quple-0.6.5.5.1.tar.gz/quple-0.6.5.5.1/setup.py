import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quple", # Replace with your own username
    version='0.6.5.5.1',
    author="Alkaid Cheng",
    author_email="chi.lung.cheng@cern.ch",
    description="A framework for quantum machine learning in high energy physics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/clcheng/quple",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[   
          'cirq',
          'numpy',
          'tensorflow',
          'tensorflow_quantum'
      ],
    python_requires='>=3.5',
)
