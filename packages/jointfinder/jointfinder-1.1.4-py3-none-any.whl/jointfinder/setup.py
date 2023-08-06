import setuptools

with open("jointfinder/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jointfinder", 
    version="1.1.4",
    author="Dr Z. Y. Tay & J. Hadi",
    author_email="januwar.hadi@singaporetech.edu.sg",
    description="Find edge-to-edge and edge-to-surface joints of planar polygons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SiDODOL/jointfinder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.5',
    install_requires=[
          'pandas', 'numpy', 'numba', 'tqdm', 'matplotlib'
      ],

)