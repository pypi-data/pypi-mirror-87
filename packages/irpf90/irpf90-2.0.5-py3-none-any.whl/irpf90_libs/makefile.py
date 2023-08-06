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


import os,sys
import irpf90_t
from command_line import command_line
irpdir = irpf90_t.irpdir
mandir = irpf90_t.mandir

FILENAME = "Makefile"
FILENAME_GITIGNORE = ".gitignore"
IRPF90_MAKE = "irpf90.make"

if sys.platform in ["linux", "linux2"]:
  ARCHIVE = "ar crs"
elif sys.platform == "darwin":
  ARCHIVE = "libtool -static -o"
else:
  print("Unknown platform. Only Linux and Darwin are supported.")
  sys.exit(-1)


######################################################################
def create():
  has_makefile = True
  try:
    file = open(FILENAME,"r")
  except IOError:
    has_makefile = False
  if has_makefile:
    return
  file = open(FILENAME,"w")
  t = """IRPF90 = irpf90  #-a -d
FC     = gfortran
FCFLAGS= -O2 -ffree-line-length-none -I .
NINJA  = ninja
ARCHIVE= %s
RANLIB = ranlib

SRC=
OBJ=
LIB=

-include %s
export

%s: $(filter-out %s%%, $(wildcard */*.irp.f)) $(wildcard *.irp.f) $(wildcard *.inc.f) Makefile 
\t$(IRPF90)
"""%(ARCHIVE,IRPF90_MAKE,IRPF90_MAKE,irpdir)
  file.write(t)
  file.close()
  create_gitignore()

######################################################################
def create_gitignore():
  has_makefile = True
  try:
    file = open(FILENAME_GITIGNORE,"r")
  except IOError:
    has_makefile = False
  if has_makefile:
    return
  file = open(FILENAME_GITIGNORE,"w")
  t = "\n".join([ irpdir, mandir, IRPF90_MAKE, 'irpf90_entities', 'tags' ])
  file.write(t)
  file.close()

######################################################################
def run_ninja():
    import ninja
    ninja.run()

######################################################################
def run_make():
    from modules import modules
    mod = []
    for m in list(modules.values()):
      mod.append(m)

    file = open(IRPF90_MAKE,'w')
    result = ""
    result += "FC+=-I %s "%(irpdir)
    for i in command_line.include_dir:
       result += "-I %s%s "%(irpdir,i)
    result += "\n"
    result += "SRC += %sirp_stack.irp.F90"%(irpdir)
    result += " %sirp_touches.irp.F90"%(irpdir)
#   result += " %sirp_checkpoint.irp.F90"%(irpdir)
    if command_line.do_openmp:
      result += " %sirp_locks.irp.F90"%(irpdir)
    if command_line.do_profile:
      result += " %sirp_profile.irp.F90"%(irpdir)
    for m in mod:
      result += " %s%s.irp.F90"%(irpdir,m.filename)
      result += " %s%s.irp.module.F90"%(irpdir,m.filename)
    print(result, file=file)

    result = "OBJ_IRP = %sirp_stack.irp.o "%(irpdir)
    for m in mod:
      if not m.is_main:
        result += " %s%s.irp.o"%(irpdir,m.filename)
        result += " %s%s.irp.module.o"%(irpdir,m.filename)
    print(result, file=file)

    print("OBJ1 = $(OBJ_IRP) $(OBJ) %sirp_touches.irp.o "%(irpdir), end=' ', file=file)
#   print >>file, " %sirp_checkpoint.irp.o"%(irpdir),
    if command_line.do_profile:
      print(" %sirp_profile.irp.o"%(irpdir), " irp_rdtsc.o", end=' ', file=file)
    if command_line.do_codelet:
      print(" irp_rdtsc.o", end=' ', file=file)
    if command_line.do_openmp:
      print(" %sirp_locks.irp.o"%(irpdir), file=file)
    else:
      print("", file=file)

    all = [x for x in modules if modules[x].is_main]
    all = [x[:-6] for x in all]
    all_o = ["%s.irp.module.o %s.irp.o"%(x,x) for x in all]
    print("ALL = %s"%(" ".join(all)), file=file)
    print("ALL_OBJ = %s"%(" ".join(all_o)), file=file)
    print("ALL_OBJ1 = $(patsubst %%, %s%%,$(notdir $(ALL_OBJ)))"%(irpdir), file=file)
    print("all:$(ALL)", file=file)
    print("\t@$(MAKE) -s move", file=file)
#    print >>file, "ifdef USE_IRPF90_A"
    for m in mod:
      if m.is_main:
        exe = m.filename
        print("%s: %s%s.irp.o %s%s.irp.module.o IRPF90_temp/irpf90.a"%(exe,irpdir,exe,irpdir,exe), file=file)
        print("\t$(FC) -o $@ %s$@.irp.o %s$@.irp.module.o IRPF90_temp/irpf90.a $(LIB)"%(irpdir,irpdir), file=file)
        print("\t@$(MAKE) -s move", file=file)
#    print >>file, "else"
#    for m in mod:
#      if m.is_main:
#        exe = m.filename
#        print >>file, "%s: %s%s.irp.o %s%s.irp.module.o $(OBJ1)"%(exe,irpdir,exe,irpdir,exe)
#        print >>file, "\t$(FC) -o $@ %s$@.irp.o %s$@.irp.module.o $(OBJ1) $(LIB)"%(irpdir,irpdir)
#        print >>file, "\t@$(MAKE) -s move"
#    print >>file, "endif"

    buffer = ""
    for m in mod:
      filename = "%s%s.irp.o: $(OBJ) %s%s.irp.module.o"%(irpdir,m.filename,irpdir,m.filename)
      needed_modules = [x for x in modules if modules[x].name in m.needed_modules]
      needed_files = [modules[x].filename for x in needed_modules]
      mds = [" %s%s.irp.module.o"%(irpdir,x) for x in needed_files]
      print(filename," ".join(mds)," ".join(m.includes), file=file)
      if not m.is_main:
        buffer += "\t - @echo '"+filename+" ".join(mds)+"' >> %sdist_Makefile\n"%(irpdir)
#   print >>file, "%sirp_touches.irp.o %sirp_checkpoint.irp.o: $(OBJ) "%(irpdir,irpdir),
    print("%sirp_touches.irp.o: $(OBJ) "%(irpdir), end=' ', file=file)
    mds = [x for x in mod if not x.is_main]
    mds = [" %s%s.irp.o %s%s.irp.o"%(irpdir,x.filename,irpdir,x.filename) for x in mds]
    print(" ".join(mds), file=file)
    if command_line.do_profile:
      print("%sirp_profile.irp.o:"%(irpdir), end=' ', file=file)
      print(" ".join(mds), file=file)
    if command_line.do_openmp:
      print("%sirp_locks.irp.o:"%(irpdir), end=' ', file=file)
      print(" ".join(mds), file=file)
    

    for dir in [ irpdir ] + [irpdir+x for x in command_line.include_dir]:
      print(dir+"%.irp.module.o: $(OBJ) "+dir+"%.irp.module.F90", file=file)
      print("\t$(FC) $(FCFLAGS) -c "+dir+"$*.irp.module.F90 -o "+dir+"$*.irp.module.o", file=file)
      print(dir+"%.irp.o: $(OBJ) "+dir+"%.irp.module.o "+dir+"%.irp.F90", file=file)
      print("\t$(FC) $(FCFLAGS) -c "+dir+"$*.irp.F90 -o "+dir+"$*.irp.o", file=file)
      print(dir+"%.irp.o: $(OBJ) "+dir+"%.irp.F90", file=file)
      print("\t$(FC) $(FCFLAGS) -c "+dir+"$*.irp.F90 -o "+dir+"$*.irp.o", file=file)
      print(dir+"%.o: %.F90", file=file)
      print("\t$(FC) $(FCFLAGS) -c $*.F90 -o "+dir+"$*.o", file=file)
      print(dir+"%.o: %.f90\n\t$(FC) $(FCFLAGS) -c $*.f90 -o "+dir+"$*.o", file=file)
      print(dir+"%.o: %.f\n\t$(FC) $(FCFLAGS) -c $*.f -o "+dir+"$*.o", file=file)
      print(dir+"%.o: %.F\n\t$(FC) $(FCFLAGS) -c $*.F -o "+dir+"$*.o", file=file)
      print(dir+"%.irp.F90: "+IRPF90_MAKE+"\n", file=file)
    print("move:\n\t@mv -f *.mod IRPF90_temp/ 2> /dev/null | DO_NOTHING=\n", file=file)
    print("IRPF90_temp/irpf90.a: $(OBJ) $(OBJ1)\n\t$(ARCHIVE) IRPF90_temp/irpf90.a $(OBJ1)\n", file=file)
    print("clean:\n\trm -rf $(EXE) $(OBJ1) IRPF90_temp/irpf90.a $(ALL_OBJ1) $(ALL)\n", file=file)
    print("veryclean:\n\t- $(MAKE) clean\n", file=file)
    print("\t- rm -rf "+irpdir+" "+mandir+" "+IRPF90_MAKE+" irpf90_entities dist tags\n", file=file)

    file.close()

######################################################################
def run():
  if command_line.do_ninja:
    run_ninja()
  else:
    run_make()

