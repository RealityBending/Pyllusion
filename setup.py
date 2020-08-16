from setuptools import setup, find_packages
import re

# ------------------
def find_version():
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format("__version__"), open('pyllusion/__init__.py').read())
    return result.group(1)
# ------------------

dependencies = ["numpy", "pandas", "Pillow", "scipy"]


setup(
    name = "pyllusion",
    description = ("A Python Module for Generating Illusions."),
    version = find_version(),
    license = "Mozilla Public License Version 2.0",
    author = "Dominique Makowski",
    author_email = "dom.makowski@gmail.com",
    maintainer = "Dominique Makowski",
    maintainer_email = "dom.makowski@gmail.com",
    packages = find_packages(),
    package_data = {
        "pyllusion.stimuli":["*.ai"],
        "pyllusion.stimuli":["*.png"]},
    install_requires = dependencies,
    dependency_links=[],
    long_description = open('README.md').read(),
    keywords = "python pyllusion visual optical illusions",
    url = "https://github.com/DominiqueMakowski/Pyllusion/",
    download_url = 'https://github.com/DominiqueMakowski/Pyllusion/zipball/master',
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers = [
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6']
)
