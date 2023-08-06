IRPF90
======
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/scemama/irpf90?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

IRPF90 is a Fortran90 preprocessor written in Python for programming using the Implicit Reference to Parameters (IRP) method. It simplifies the development of large fortran codes in the field of scientific high performance computing.

Dependencies
------------

- GNU make (>= 3.81 recommended)
- Python >2.6
- Any Fortran 90 compiler (Intel recommended)

Installing IRPF90
-----------------

``pip install irpf90``

or

``${IRPF90_HOME}`` is the location of your irpf90 directory::

``` bash
cd ${IRPF90_HOME}
make
cat << EOF >> ${HOME}/.bash_profile
export PYTHONPATH=${IRPF90_HOME}/src:${PYTHONPATH}
export PATH=${IRPF90_HOME}/bin:${PATH}
export MANPATH=${IRPF90_HOME}/man:${MANPATH}
EOF
source ${HOME}/.bash_profile
```


Using IRPF90
------------

In an empty directory, run:

``` bash
irpf90 --init
```

This command creates a new Makefile suitable for most irpf90 projects.
Now you can start to program using irpf90.


Web Site
--------

http://irpf90.ups-tlse.fr

