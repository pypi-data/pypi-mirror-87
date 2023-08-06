import sys
import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    readme = ''

version = '0.2.4'

install_requires = [
    'Django',
]

tests_require = [
    'Django',
    'mock',
]

try:
    PY2 = sys.version_info[0] == 2
    LTE_PY26 = PY2 and (7 > sys.version_info[1])
    PY3 = sys.version_info[0] == 3

    if LTE_PY26:
        install_requires.append('importlib')
except:
    pass

setup(
    name='django-nine',
    version=version,
    description="Version checking library.",
    long_description="{0}".format(readme),
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/barseghyanartur/django-nine/issues",
        "Documentation": "https://django-nine.readthedocs.io/",
        "Source Code": "https://github.com/barseghyanartur/django-nine",
        "Changelog": "https://django-nine.readthedocs.io/"
                     "en/latest/changelog.html",
    },
    keywords='django, compatibility',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://github.com/barseghyanartur/django-nine/',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    license='GPL-2.0-only OR LGPL-2.1-or-later',
    install_requires=install_requires,
    tests_require=tests_require,
    package_data={},
    include_package_data=True,
)
