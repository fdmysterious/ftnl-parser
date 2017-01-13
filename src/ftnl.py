#!/usr/bin/env python
"""
*************
*-=ftnl.py=-*
*************

Author      : Florian Dupeyron (My?terious)
Description : FTNL Main program file
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
import argparse

import parser
import output
import os
#-=End of section=-#

#-=Global configuration=-#
outputs = {
    #"html": output.HTMLOutput(),
    "mmap": output.MMapOutput(),
    "freeplane": output.FreeplaneOutput()
}
default_output = "html"
#-=End of section=-#

cmdargs = argparse.ArgumentParser(description="Simple parser for the FTNL language")

cmdargs.add_argument("-o", "--output", default="freeplane", choices=outputs.keys(), help="Choose which output module to use")
cmdargs.add_argument("FILE", help="Path to the input file")
cmdargs.add_argument("OUTFILE", help="Path to the output file")
cmdargs.add_argument("--debug", help="Enable debug messages")

args = cmdargs.parse_args()

#TODO : Exception Handling
with open(args.FILE, "r") as f:
    with open(args.OUTFILE, "w") as g:
        g.write(outputs[args.output].output_node(parser.from_stream(f)))

