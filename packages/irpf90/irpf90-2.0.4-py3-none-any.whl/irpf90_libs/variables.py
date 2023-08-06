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


from variable import *
from irpf90_t import *
from command_line import command_line
from util import *
import error

forbidden_names = ["type", "double precision", "integer", "use", "character", "real"]

######################################################################
def create_variables():
  from preprocessed_text import preprocessed_text
  result = {}
  icount = 0
  for filename, text in preprocessed_text:
    buffer = []
    inside = False
    for line in text:
      if type(line) == Begin_provider:
        inside = True
      if inside:
        buffer.append(line)
      if type(line) == End_provider:
        inside = False
        icount += 1
        v = Variable(buffer,icount)
        if v.name in result:
          print("Warning: Duplicate provider for %s in"%(v.name))
          print("- ", v.line.filename[0], " line ", v.line.i)
          print("- ", result[v.name].line.filename[0], " line ", result[v.name].line.i)
          print("Choosing first version")
        if v.name in forbidden_names:
           error.fail(line,"A variable can't be named %s"%(v.name))
        result[v.name] = v
        for other in v.others:
          if other in result:
            print("Warning: Duplicate provider for %s in"%(other))
            print("- ", v.line.filename[0], " line ", v.line.i)
            print("- ", result[other].line.filename[0], " line ", result[other].line.i)
            print("Choosing first version")
          result[other] = Variable(buffer,icount,other)
        buffer = []
  return result

variables = create_variables()

######################################################################
def build_use(vars):
  result = ["  use %s"%(variables[x].fmodule) for x in vars]
  result = make_single(result)
  return result

######################################################################
def call_provides(vars,opt=False):
  vars = make_single( [variables[x].same_as for x in vars] )
  if opt:
    all_children = flatten( [variables[x].children for x in vars])
    vars = [x for x in vars if x not in all_children]
  def fun(x):
    result = []
    result += [ \
    "  if (.not.%s_is_built) then"%(x) ]
    result += [ \
    "    call provide_%s"%(x) ]
    result += [ \
    "  endif" ]
    return result

  result = flatten ( list(map (fun, vars)) )
  return result

######################################################################
if __name__ == '__main__':
  for v in list(variables.keys()):
    print(v)
