import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PteraSoftware",
    version="0.3.1",
    author="Cameron Urban",
    author_email="camerongurban@gmail.com",
    description="This is an open-source, unsteady aerodynamics solver for analyzing flapping-wing flight.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camurban/pterasoftware",
    packages=setuptools.find_packages(
        exclude=[".github", "docs", "examples", "legacysolvers", "tests",]
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="aerospace computational-biology airplane cfd computational-fluid-dynamics aerodynamics aeronautics aerospace-engineering unmanned-aerial-system aircraft-design unmanned-aerial-vehicle ornithopter ornithology vortex-lattice-method unsteady-flows vlm potential-flow",
    python_requires=">= 3.7.6, < 3.8",
    install_requires=[
        "matplotlib >= 3.2.2, < 4.0.0",
        "numpy >= 1.18.5, < 1.19.0",
        "pyvista >= 0.25.3, < 1.0.0",
        "scipy >= 1.5, < 2.0",
    ],
)
