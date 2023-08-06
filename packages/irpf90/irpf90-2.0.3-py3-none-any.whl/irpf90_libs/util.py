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

import os
NTHREADS=1 #int(os.getenv('OMP_NUM_THREADS',1))

def strip(x):
  return x.strip()

def lower(x):
  return x.lower()

def same_file(filename,txt):
  assert isinstance(filename,str)
  if (type(txt) == list):
    buffer = ''.join(txt)
  else:
    buffer = txt

  try:
    file = open(filename,"r")
  except IOError:
    return False
  stream = file.read()
  file.close()

  if len(stream) != len(buffer):
    return False
  if stream != buffer:
    return False
  return True

def build_dim(dim):
  if len(dim) == 0:
    return ""
  else:
    return "(%s)"%( ",".join(dim) )

def build_dim_colons(v):
  d = v.dim
  if d == []:
    return ""
  else:
    x = [":" for x in d]
    return "(%s)"%(','.join(x))


import error
def find_subname(line):
  buffer = line.lower
  if not buffer.endswith(')'):
    buffer += "()"
  buffer = buffer.split('(')
  buffer = buffer[0].split()
  if len(buffer) < 2:
    error.fail(line,"Syntax Error")
  return buffer[-1]

def make_single(l):
  d = {}
  for x in l:
   d[x] = True
  return list(d.keys())

def flatten(l):
  if type(l) == list:
    result = []
    for i in range(len(l)):
      elem = l[i]
      result += flatten(elem)
    return result
  else:
    return [l]

def dimsize(x):
  assert isinstance(x,str)
  buffer = x.split(':')
  if len(buffer) == 1:
    return x
  else:
    assert len(buffer) == 2
    size = ""
    b0, b1 = buffer
    if b0.replace('-','').isdigit() and b1.replace('-','').isdigit():
      size = str( int(b1) - int(b0) + 1 )
    else:
      if b0.replace('-','').isdigit():
        size = "(%s) - (%d)"%(b1,int(b0)-1)
      elif b1.replace('-','').isdigit():
        size = "(%d) - (%s)"%(int(b1)+1,b0)
      else:
        size = "(%s) - (%s) + 1"%(b1,b0)
    return size

def put_info(text,filename):
  assert type(text) == list
  if len(text) > 0:
    assert type(text[0]) == tuple
    from irpf90_t import Line
    assert type(text[0][0]) == list
    assert isinstance(text[0][1], Line)
    lenmax = 80 - len(filename)
    format = "%"+str(lenmax)+"s ! %s:%4s"
    for vars,line in text:
      line.text = format%(line.text.ljust(lenmax),line.filename,str(line.i))
  return text

import pickle as pickle
import os, sys
def parallel_loop(f,source):
  pidlist = list(range(NTHREADS))

  src = [ [] for i in range(NTHREADS) ]
  index = 0
  try:
    source = [(len(x[1]),(x[0], x[1])) for x in source]
    source.sort()
    source = [x[1] for x in source]
  except:
    pass
  for i in source:
    index += 1
    if index == NTHREADS:
      index = 0
    src[index].append(i)

  thread_id = 0
  fork = 1
  r = list(range(0,NTHREADS))
  for thread_id in range(1,NTHREADS):
    r[thread_id], w = os.pipe()
    fork = os.fork()
    if fork == 0:
      os.close(r[thread_id])
      w = os.fdopen(w,'w')
      break
    else:
      os.close(w)
      r[thread_id] = os.fdopen(r[thread_id],'r')
      pidlist[thread_id] = fork
      thread_id = 0

  result = []
  for filename, text in src[thread_id]:
    result.append( (filename, f(filename,text)) )
  result = sorted(result, key=lambda x: x[0])

  if fork == 0:
    pickle.dump(result,w,-1)
    w.close()
    os._exit(0)
  
  for i in range(1,NTHREADS):
    result += pickle.load(r[i])
    r[i].close()
    os.waitpid(pidlist[i],0)[1] 

  return result



if __name__ == '__main__':
  print("10",dimsize("10")) #-> "10"
  print("0:10",dimsize("0:10")) # -> "11"
  print("0:x",dimsize("0:x"))  # -> "x+1"
  print("-3:x",dimsize("-3:x"))  # -> "x+1"
  print("x:y",dimsize("x:y"))  # -> "y-x+1"
  print("x:5",dimsize("x:5"))  # -> "y-x+1"

