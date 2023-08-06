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


from variable  import Variable
from variables import variables
from subroutine  import Sub
from subroutines import subroutines
from irpf90_t  import *
from util import *


def do_print_short(file,var):
  """Makes a short print, as in irpf90_entities"""
  assert type(var) == Variable
  print("%s : %s :: %s %s"%( \
   var.line.filename[0].ljust(35),
   var.type.ljust(30),
   var.name.ljust(25),
   build_dim(var.dim) ), file=file)

######################################################################
def process_doc(file,line):
  assert type(line) == str
  line = line.strip()
  if line == "":
    line = ".br"
  print(line, file=file)

######################################################################
def process_deps(file,l):
  assert type(l) == list
  for v in l:
    print("%s\n.br"%(v,), file=file)

######################################################################
def process_types(file,var):
  assert type(var) == Variable
  vars = [var.name] + var.others
  for var in vars:
    name = var
    var = variables[var]
    Type = var.type
    dim = build_dim(var.dim)
    print("%s\t:: %s\t%s"%(Type,name,dim), file=file)

######################################################################
def do_print(var):
  assert type(var) == Variable
  filename = var.line.filename[0]
  name = var.name
  file = open("%s%s.l"%(mandir,var.name), "w")
  print('.TH "IRPF90 entities" l %s "IRPF90 entities" %s'%(name,name), file=file)
  if var.same_as != var.name:
    var = variables[var.same_as]
  print(".SH Declaration", file=file)
  print(".nf", file=file)
  process_types(file,var)
  print(".ni", file=file)
  if var.doc != []:
   print(".SH Description", file=file)
   for l in var.doc:
     process_doc(file,l)
  print(".SH File\n.P", file=file)
  print(filename, file=file)
  if var.needs != []:
    var.needs.sort()
    print(".SH Needs", file=file)
    process_deps(file,var.needs)
  if var.needed_by != []:
    var.needed_by.sort()
    print(".SH Needed by", file=file)
    process_deps(file,var.needed_by)
  print(".SH Instability factor", file=file)
  fo = len(var.children)
  fi = len(var.parents)
  print("%5.1f %%"%(100.* (fi / (fi+fo+.000001) )), file=file)
  print(".br", file=file)
  file.close()

######################################################################
def do_print_rst(var):
  """Print providers in a format suitable for sphinx"""
  assert type(var) == Variable
  filename = var.line.filename[0]
  name = var.name
  file = open("%s%s.rst"%(mandir,var.name), "w")
  print(".. c:var:: %s\n"%(var.name.lower()), file=file)
  print("", file=file)
  print("    File : :file:`"+filename+"`", file=file)
  print("", file=file)
  print("    .. code:: fortran", file=file)
  print("", file=file)
  if var.same_as != var.name:
    var = variables[var.same_as]
  for v in [var.name] + var.others:
    name = v
    v = variables[v]
    Type = v.type
    dim = build_dim(v.dim)
    print("        %s\t:: %s\t%s"%(Type,name,dim), file=file)
  print("", file=file)
  print("", file=file)

  if var.doc != []:
    d = []
    for text in var.doc:
        text_old = None
        while text_old != text:
            text_old = text
            text = text.replace("$",":math:`",1).replace("$","` ",1)
        d.append(text)
    loop = True
    while loop:
      maxlen=0
      for l in d:
        ll = len(l)
        maxlen = max(ll,maxlen)
        if ll > 0 and l[0] != ' ':
          loop = False
          break
      loop = loop and maxlen > 0
      if loop:
        d = [ l[1:] for l in d ]
    for line in d:
        print("    "+line, file=file)
  print("", file=file)
  if var.needs != []:
    var.needs.sort()
    print("    Needs:", file=file)
    print("", file=file)
    print("    .. hlist::", file=file)
    print("       :columns: 3", file=file)
    print("", file=file)
    for v in var.needs:
        print("       * :c:data:`%s`"%(variables[v].same_as.lower(),), file=file)
    print("", file=file)
  if var.needed_by != []:
    var.needed_by.sort()
    print("    Needed by:", file=file)
    print("", file=file)
    print("    .. hlist::", file=file)
    print("       :columns: 3", file=file)
    print("", file=file)
    for v in var.needed_by:
        print("       * :c:data:`%s`"%(variables[v].same_as.lower(),), file=file)
  print("", file=file)
  file.close()

######################################################################
def process_declaration_subroutine(file, sub):
  print(sub.line.text.split('!')[0].strip(), file=file)

# for line in sub.text:
######################################################################
def do_print_subroutines(sub):
  assert type(sub) == Sub
  filename = sub.line.filename
  name = sub.name
  file = open("%s%s.l"%(mandir,sub.name), "w")
  print('.TH "IRPF90 entities" l %s "IRPF90 entities" %s'%(name,name), file=file)
  print(".SH Declaration", file=file)
  print(".nf", file=file)
  process_declaration_subroutine(file,sub)
  print(".ni", file=file)
  if sub.doc != []:
   print(".SH Description", file=file)
   for l in sub.doc:
     process_doc(file,l)
  print(".SH File\n.P", file=file)
  print(filename, file=file)
  if sub.needs != []:
    sub.needs.sort()
    print(".SH Needs", file=file)
    process_deps(file,sub.needs)
  if sub.called_by != []:
    sub.called_by.sort()
    print(".SH Called by", file=file)
    process_deps(file,sub.called_by)
  if sub.calls != []:
    sub.calls.sort()
    print(".SH Calls", file=file)
    process_deps(file,sub.calls)
  if sub.touches != []:
    sub.touches.sort()
    print(".SH Touches", file=file)
    process_deps(file,sub.touches)
  print(".SH Instability factor", file=file)
  fo = len(sub.needs)+len(sub.calls)+len(sub.touches)
  fi = len(sub.called_by)
  print("%5.1f %%"%(100.* (fi / (fi+fo+.000001) )), file=file)
  print(".br", file=file)
  file.close()

######################################################################
def do_print_subroutines_rst(sub):
  """Print subroutines in a format suitable for sphinx"""
  assert type(sub) == Sub
  filename = sub.line.filename
  name = sub.name
  file = open("%s%s.rst"%(mandir,sub.name), "w")
  print(".. c:function:: %s:\n"%(sub.name.lower()), file=file)
  print("", file=file)
  print("    File : :file:`"+filename+"`", file=file)
  print("", file=file)
  print("    .. code:: fortran", file=file)
  print("", file=file)
  print("        "+sub.line.text.split('!')[0].strip(), file=file)
  print("", file=file)
  print("", file=file)
  if sub.doc != []:
    d = list(sub.doc)
    loop = True
    while loop:
      maxlen=0
      for l in d:
        ll = len(l)
        maxlen = max(ll,maxlen)
        if ll > 0 and l[0] != ' ':
          loop = False
          break
      loop = loop and maxlen > 0
      if loop:
        d = [ l[1:] for l in d ]
    for l in d:
        print("    "+l, file=file)
  print("", file=file)
  if sub.needs != []:
    sub.needs.sort()
    print("    Needs:", file=file)
    print("", file=file)
    print("    .. hlist::", file=file)
    print("       :columns: 3", file=file)
    print("", file=file)
    for v in sub.needs:
        print("       * :c:data:`%s`"%(variables[v].same_as.lower(),), file=file)
    print("", file=file)
  if sub.called_by != []:
    sub.called_by.sort()
    print("    Called by:", file=file)
    print("", file=file)
    print("    .. hlist::", file=file)
    print("       :columns: 3", file=file)
    print("", file=file)
    for v in sub.called_by:
        if v in subroutines:
            print("       * :c:func:`%s`"%(v.lower(),), file=file)
        elif v in variables:
            print("       * :c:data:`%s`"%(variables[v.lower()].same_as.lower(),), file=file)
    print("", file=file)
  if sub.calls != []:
    sub.calls.sort()
    print("    Calls:", file=file)
    print("", file=file)
    print("    .. hlist::", file=file)
    print("       :columns: 3", file=file)
    print("", file=file)
    for v in sub.calls:
        print("       * :c:func:`%s`"%(v.lower(),), file=file)
    print("", file=file)
  if sub.touches != []:
    sub.touches.sort()
    print("    Touches:", file=file)
    print("", file=file)
    print("    .. hlist::", file=file)
    print("       :columns: 3", file=file)
    print("", file=file)
    for v in sub.touches:
        print("       * :c:data:`%s`"%(variables[v.lower()].same_as.lower(),), file=file)
    print("", file=file)
  file.close()

######################################################################
def run():
  import parsed_text
  import os,sys
  pid1 = os.fork()
  if pid1 == 0:
    for v in list(variables.values()):
      do_print(v)
      do_print_rst(v)
    for s in list(subroutines.values()):
      do_print_subroutines(s)
      do_print_subroutines_rst(s)
    sys.exit(0)

  pid2 = os.fork()
  if pid2 == 0:
    tags = []
    l = list(variables.keys())
    file = open("irpf90_entities","w")
    l.sort()
    for v in l:
      do_print_short(file,variables[v])
      line = variables[v].line
      tags.append( '%s\t%s\t%d\n'%(v,line.filename[0],line.i) )
    file.close()
    l = list(subroutines.keys())
    for v in l:
      line = subroutines[v].line
      tags.append('%s\t%s\t%d\n'%(v,line.filename,line.i))
    tags.sort()
    file = open("tags","w")
    for line in tags:
      file.write(line)
    file.close()

#    # Create emacs tags
#    tags = {}
#    l = list(variables.keys())
#    for v in l:
#      line = variables[v].line
#      if line.filename[0] not in tags:
#        tags[line.filename[0]] = []
#      tags[line.filename[0]].append( (v,line) )
#    l = list(subroutines.keys())
#    for v in l:
#      line = subroutines[v].line
#      if line.filename not in tags:
#        tags[line.filename] = []
#      tags[line.filename].append( (v,line) )
#
#    file = open("TAGS","w")
#    for f in tags:
#      tags[f].sort()
#      text = ""
#      for v, line in tags[f]:
#        text += "%s\x7f%s\x01%d,0\n"%(line.text.split('!')[0].rstrip(),v,line.i)
#      file.write("\x0c\n%s,%d\n"%(f, len(text)))
#      file.write(text)
#    file.close()

    sys.exit(0)

  os.waitpid(pid1,0)
  os.waitpid(pid2,0)

######################################################################
if __name__ == '__main__':
  run()
