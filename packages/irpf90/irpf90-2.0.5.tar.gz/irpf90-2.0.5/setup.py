import sys

import setuptools
import version

with open("README.md", "r") as fh:
    long_description = fh.read()

v = version.version

setuptools.setup(
  name = 'irpf90',
  version = v,
  scripts = ["irpf90", "irpman", "irpf90_indent"],
  author = 'Anthony Scemama',
  author_email = 'scemama@irsamc.ups-tlse.fr',
  description = 'IRPF90 is a Fortran90 preprocessor written in Python for programming using the Implicit Reference to Parameters (IRP) method. It simplifies the development of large fortran codes in the field of scientific high performance computing.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://irpf90.ups-tlse.fr",
  download_url = f'https://gitlab.com/scemama/irpf90/-/archive/v{v}/irpf90-v{v}.tar.gz',
  packages=setuptools.find_packages(),
  classifiers=[
         "Programming Language :: Python :: 3",
         "Programming Language :: Fortran",
         "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
         "Operating System :: POSIX :: Linux",
     ],
  keywords = ['programming', 'fortran', 'IRP'], 
 )
