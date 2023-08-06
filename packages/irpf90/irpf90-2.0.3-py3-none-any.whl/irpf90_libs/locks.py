#!/usr/bin/env python3
#   IRPF90 is a Fortran90 preprocessor written in Python for programming using
#   the Implicit Reference to Parameters (IRP) method.
#   Copyright (C) 2009 Anthony SCEMAMA 
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#   Anthony Scemama
#   LCPQ - IRSAMC - CNRS
#   Universite Paul Sabatier
#   118, route de Narbonne      
#   31062 Toulouse Cedex 4      
#   scemama@irsamc.ups-tlse.fr


from command_line import command_line

from irpf90_t import *
from util import *
from variables import variables
FILENAME=irpdir+'irp_locks.irp.F90'

def create():
  out = []
  l = list(variables.keys())
  l.sort
  for v in l:
    var = variables[v]
    out += var.locker

  out += [
"subroutine irp_init_locks_%s()"%(irp_id),
" implicit none" ]
  for v in l:
    out += [ "  call irp_lock_%s(.True.)"%v ]
    out += [ "  call irp_lock_%s(.False.)"%v ]
  out += [ "end subroutine" ]
  out = ["%s\n"%(x) for x in out]
  if not same_file(FILENAME,out):
    file = open(FILENAME,'w')
    file.writelines(out)
    file.close()

if __name__ == '__main__':
  create()
  
