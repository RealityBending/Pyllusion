import re

from setuptools import find_packages, setup


# ------------------
def find_version():
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format("__version__"),
        open("pyllusion/__init__.py").read(),
    )
    return result.group(1)


# ------------------

dependencies = ["numpy", "pandas", "Pillow>=10.1.0", "scipy>=1.13.0"]
setup_requirements = ["numpy"]
test_requirements = dependencies + ["pytest", "pytest-cov", "matplotlib", "coverage", "scikit-image"]


setup(
    # Info
    name="pyllusion",
    description=("A Parametric Framework to Generate Visual Illusions."),
    version=find_version(),
    license="Mozilla Public License Version 2.0",
    # The name and contact of a maintainer
    author="Dominique Makowski",
    author_email="dom.makowski@gmail.com",
    maintainer="Dominique Makowski",
    maintainer_email="dom.makowski@gmail.com",
    # Dependencies
    install_requires=dependencies,
    setup_requires=setup_requirements,
    extras_require={"test": test_requirements},
    dependency_links=[],
    # Misc
    packages=find_packages(),
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    keywords="python pyllusion visual optical illusions",
    url="https://github.com/RealityBending/Pyllusion/",
    download_url="https://github.com/RealityBending/Pyllusion/zipball/master",
    python_requires=">=3.9",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
