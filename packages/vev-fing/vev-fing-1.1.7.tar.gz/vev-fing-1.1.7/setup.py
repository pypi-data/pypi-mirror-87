from setuptools import setup, find_packages
from io import open
from os import path
import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
install_requires = [
    'matplotlib==3.2.1',
    'numpy==1.18.4',
    'pandas==0.25.3',
    'Pillow==7.1.2',
    'scikit-learn==0.22.2.post1',
    'scipy==1.4.1',
    'pyqt5==5.15',
    'pyqtchart==5.15',
    'dnspython==1.16.0',
    'fastparquet==0.4.0',
    'pymongo==3.11.0',
    'pyarrow==0.16.0',
    'jsonschema==3.2.0',
    'pyts==0.11.0'
    ]

setup (
 name = 'vev-fing',
 description = 'Visualization and Evolution of ARN Virus',
 version = '1.1.7',
 packages = find_packages(), # list of all packages
 install_requires = install_requires,
 python_requires='>=3.6', # any python greater than 3.6
 entry_points={
        'console_scripts': [
            'vev = src.vev:main',
        ],
    },
 include_package_data=True,
 author="Federico Aicardi,Rodrigo Cespedes",
 keyword="ARN,VIRUS,Evolution,Analysis,Visualization",
 long_description=README,
 long_description_content_type="text/markdown",
 license='MIT',
 url='', 
  author_email='vev-fing@gmail.com',
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ]
)
