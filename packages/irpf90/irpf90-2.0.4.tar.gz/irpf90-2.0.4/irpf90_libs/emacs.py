"""
IRPF90 is a Fortran90 preprocessor written in Python for programming using
the Implicit Reference to Parameters (IRP) method.
Copyright (C) 2009 Anthony SCEMAMA

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

This script handles the files needed to use the IRPF90 Emacs mode. This
config used the emacs package `use-package`
 (https://jwiegley.github.io/use-package/).
The user is responsible for its installing and configuring it.
Contributed by Ramon L. Panades-Barrueta (https://tinyurl.com/y6qvjmxg ).

"""
import os
import shutil


def install():
    """Installs the irp-mode in Emacs"""
    # Check user Emacs config
    emacs_init = [*map(lambda x: os.environ["HOME"] + x,
                       ["/.emacs.d/inil.el", "/.emacs"])]

    emacs_dir = os.environ["HOME"] + "/.emacs.d"
    os.makedirs(f"{emacs_dir}/lib", exist_ok=True)

    emacs = emacs_init[0] if os.access(
        emacs_init[0], os.F_OK) else emacs_init[1]

    # Add support for irp-mode and Yasnippets
    with open(emacs, "a") as emfil:
        emfil.write("\n")
        emfil.write(";; Use Yasnippets\n")
        emfil.write("(use-package yasnippet\n")
        emfil.write(" :ensure t\n")
        emfil.write(" :config\n")
        emfil.write(" (yas-global-mode 1))\n")
        emfil.write("\n")
        emfil.write(";; Use irp-mode\n")
        emfil.write("(use-package irp-mode\n")
        emfil.write(r""" :mode ("\\.irp.f\\'")""")
        emfil.write(f"""\n :load-path "{emacs_dir}/lib")\n""")

    # Copy irp-mode files
    workd = os.path.abspath(os.path.dirname(__file__))
    with open(f"{workd}/irp-mode.el", 'r') as f_in:
        with open(f"{emacs_dir}/lib/irp-mode.el", 'w') as f_out:
            f_out.write(f_in.read())

    # Snippets
    os.makedirs(f"{emacs_dir}/snippets/irp-mode/", exist_ok=True)
    snips = os.listdir(f"{workd}/irp_snippets")
    for fil in snips:
        shutil.copy(f"{workd}/irp_snippets/{fil}",
                    f"{emacs_dir}/snippets/irp-mode/")


if __name__ == "__main__":
    install()
