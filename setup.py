from setuptools import setup, find_packages
import re

# ------------------
def find_version():
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format("__version__"), open('pyllusion/__init__.py').read())
    return result.group(1)
# ------------------

dependencies = ["numpy", "pandas", "Pillow", "scipy"]
setup_requirements = ["pytest-runner", "numpy"]
test_requirements = dependencies + [
    "pytest",
    "coverage"
]


setup(
    # Info
    name = "pyllusion",
    description = ("A Parametric Framework to Generate Visual Illusions."),
    version = find_version(),
    license = "Mozilla Public License Version 2.0",
    
    # The name and contact of a maintainer
    author = "Dominique Makowski",
    author_email = "dom.makowski@gmail.com",
    maintainer = "Dominique Makowski",
    maintainer_email = "dom.makowski@gmail.com",
    
    # Dependencies
    install_requires=dependencies,
    setup_requires=setup_requirements,
    test_suite="pytest",
    tests_require=test_requirements,
    extras_require={"test": test_requirements},
    dependency_links=[],
    
    # Misc
    packages = find_packages(),
    package_data = {
        "pyllusion.stimuli":["*.ai"],
        "pyllusion.stimuli":["*.png"]},
    long_description = open('README.md', encoding='utf8').read(),
    keywords = "python pyllusion visual optical illusions",
    url = "https://github.com/DominiqueMakowski/Pyllusion/",
    download_url = 'https://github.com/DominiqueMakowski/Pyllusion/zipball/master',
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
