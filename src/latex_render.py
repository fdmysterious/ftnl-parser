"""
*********************
*-=latex_render.py=-*
*********************

Author      : Florian Dupeyron (My?terious)
Description : Configuration of node Attachments

Note : This thing's kinda dirty, made for testing purposes.
"""

# (c) 2016 Florian Dupeyron (florian.dupeyron<at>mugcat<dot>fr)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#-=Imports=-#
import sys
import os
import shutil
import time
import tempfile
import subprocess

import latex_template
#-=End of section=-#

#-=Exception=-#
class LatexRenderException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
#-=End of section=-#

#-=LatexPDFRenderer=-#
class LatexPDFRenderer:
    """
    Basic class for rendering LaTeX code.
    """
    def __init__(self):
        self.conversion_function = None

    #-=Chain modifiers=-#
    def chain_conversion_function(self, conversion_function):
        self.conversion_function = conversion_function
        return self
    #-=End of section=-#

    def render(self, s, destDir):
        """
        Renders the given math string to a file in the output
        directory

        :param s : the Stirng to render
        :param destDir : the Ouptut directory
        :return: relative path to new file
        """

        #-=Variables=-#
        err = None # err is filled with eventual exception
        tmpdir  = ""

        outfile = ""
        #-=End of section=-#

        try:
            #-=Creating directories=-#
            if not os.path.exists(destDir) : os.makedirs(destDir)
            #--Generating name
            epochstr = str(time.time()) #Epoch thing

            #--let's do it !
            tmpdir = tempfile.mkdtemp(epochstr)
            #-=End of section=-#

            #-=Creating file=-#
            #TODO : Optimisation
            f = open(tmpdir + "/in.tex", "a")
            f.write(latex_template.s.format(s))
            f.close()
            #-=End of section=-#

            #-=Generating PDF Output=-#
            #--Generation
            if subprocess.call(["pdflatex", "-halt-on-error", "-output-directory", tmpdir, tmpdir + "/in.tex"], stdout=sys.stderr) > 0: raise LatexRenderException("Render failed")
            #--crop
            outfile = "/{0}.pdf".format(epochstr)
            if subprocess.call(["pdfcrop", "-margins", "2", tmpdir + "/in.pdf", tmpdir + outfile], stdout=sys.stderr) > 0: raise LatexRenderException("Cropping PDF failed")
            #-=End of section=-#

            #-=Calling conversion function=-#
            if self.conversion_function is not None: outfile = self.conversion_function(tmpdir, outfile, epochstr)
            #-=End of section=-#

            #-=Copying to destination=-#
            shutil.copyfile(tmpdir + outfile, destDir + outfile)
            #-=End of section=-#

        except Exception as e:
            err = e
        except IOError as e:
            err = e
        except LatexRenderException as e:
            err = e

        #-=Removing temp directory=-#
        if(tmpdir): shutil.rmtree(tmpdir)
        #-=End of section=-#

        #-=Raise exception ?=-#
        if err is not None : raise err
        #-=End of section=-#

        #-=Return new file name=-#
        return outfile
        #-=End of section=-#
#-=End of section=-#

#-=LatexPngRenderer=-#
class LatexPngRenderer(LatexPDFRenderer):
    def _convPng(self, tmpdir, infile, epochstr):
        #-=Generating new file name=-#
        outfile = "/{0}.png".format(epochstr)
        #-=End of section=-#

        #-=Calling convert command=-#
        if subprocess.call(["convert", "-density", "300", tmpdir + infile, "-quality", "90", tmpdir + outfile], stdout=sys.stderr) > 0 : raise LatexRenderException("Conversion error")
        #-=End of section=-#

        return outfile


    def __init__(self):
        self.conversion_function = self._convPng
#-=End of section=-#

#-=Glboal renderers=-#
pdf = LatexPDFRenderer()
png = LatexPngRenderer()
#-=End of section=-#
