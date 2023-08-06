import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spiffy", # Replace with your own username
    version="0.0.10",
    author="Arthur Reis",
    author_email="arpereis@gmail.com",
    description="Space Interferometer Python Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurpreis/spiffy",
    packages=setuptools.find_packages(),
    #packages = setuptools.find_namespace_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.6',
    install_requires = [ 'jupyterlab', 'matplotlib',
                          'notebook', 'numpy', 'PyQt5', 'sympy',
                         'vtk','mayavi',
                          ]
)