from setuptools import setup, find_packages
import os
 
__version__ = '0.0.1'

# Read requirements from requirements.txt
with open(os.getcwd()+'/strform/requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
  name = 'strform',     
  packages = find_packages(),  
  version = __version__,      
  license='',    
  description = 'STR sequence compression and formatting',
  author = 'Alexander YY Liu',
  author_email = 'yliu575@aucklanduni.ac.nz',  
  url = 'https://github.com/alexyyl/STRform', 
  download_url = 'https://github.com/alexyyl/STRform/releases/tag/v_%s.tar.gz' % __version__, 
  keywords = ['forensic STR', 'bracketed repeat formatting'], 
  python_requires='>=3.6',
  install_requires=requirements,
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Programming Language :: Python :: 3.6',
  ],
  package_data = {'': ['', '*', '*/*']},
)
