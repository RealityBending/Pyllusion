from setuptools import setup, find_packages
import re

# ------------------
def find_version():
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format("__version__"), open('pyllusion/__init__.py').read())
    return result.group(1)
# ------------------

setup(
name = "pyllusion",
description = ("An Python Module for Generating Visual Illusions."),
version = find_version(),
license = "Mozilla Public License Version 2.0",
author = "Dominique Makowski",
author_email = "dom.makowski@gmail.com",
maintainer = "Dominique Makowski",
maintainer_email = "dom.makowski@gmail.com",
packages = find_packages(),
package_data = {
	"pyllusion.stimuli":["*.ai"],
	"neuropsydia.stimuli":["*.png"]},
install_requires = [
    'neuropsydia > 1.0.0'],
dependency_links=[
	"https://github.com/neuropsychology/Neuropsydia.py/zipball/master"],
long_description = open('README.rst').read(),
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
