"""
***************
*-=parser.py=-*
***************

Author      : Florian Dupeyron (My?terious)
Description : Contains parse functions
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
import re
import os

from formatString import FormatString
from node import Node

import nodeProperties
import nodeAttachments
#-=End of section=-#

#-=ParseException class=-#
class ParseException(Exception):
    def __init__(self, linenum, value):
        self.value = "line " + str(linenum) + " : " + value

    def __str__(self):
        return repr(self.value)
#-=End of section=-#

#-=Some ugly global vars=-#
formatted_reg  = re.compile(r"(\*\*?|\$)([^\*\$]+)\1")
tablevel_reg   = re.compile(r"^\t*")
newline_reg    = re.compile(r"^\s*$")
property_reg   = re.compile(r"^(\w+)(?:\s*\=\s*(\w+))?$")
title_reg      = re.compile(r"\s*\[(.+)\]\s*")
attachment_reg = re.compile(r"\s*(\w+)\s*")
clean_reg      = re.compile(r"\s*$")

#TODO : Move this elsewhere
type_tab      = {"*": "emph", "**": "critical", "/": "italic", "": "plain"}

#--Context vars
#-=End of section=-#

#-=Utility functions=-#
#TODO : Space indent
#TEST : 0 tablevel, 1 tablevel, 2 tablevel
def tablevel(s):
    """
    Utility function that returns the indent level of the line

    :param s: The raw string
    :return: The tablevel
    """
    return len(tablevel_reg.match(s).group())

#TEST : 0 tablevel, 1 tablevel, 1 space, with content
def is_newline(s):
    """
    Test if the string is an empty line

    :param s: The raw string
    :return: A boolean value
    """

    return newline_reg.match(s) is not None 
#-=End of section=-#

#-=Parse formatted=-#
#TEST : Empty string, plain string, string with bold
#TODO : Paragraph support
def formatted(s):
    """
    Converts a standard string written in FTNL language
    to some internal formatted string structure

    :param s: the string to convert
    :return: a FormatString corresponding to the decoded string, empty if no content
    """
    r  = FormatString().chain_type("plain")
    m  = formatted_reg.search(s)
    st = 0
    while m is not None:
        #-=Adding previous=-#
        previous = s[st:m.start()]
        if previous: r.append(FormatString.create_plain(previous))
        #-=End of section=-#

        #-=Adding current=-#
        if(m.group(1) == "$"):
            c = FormatString().create_math(m.group(2))
        else:
            c = FormatString().chain_type(type_tab[m.group(1)]).chain_content(formatted(m.group(2)))

        r.append(c)
        #-=End of section=-#

        #-=Searching next=-#
        st = m.end()
        m  = formatted_reg.search(s, st)
        #-=End of section=-#

    #-=Adding remaining content=-#
    if s[st:] != "": r.append(FormatString.create_plain(s[st:])) 
    #-=End of section=-#

    return r
#-=End of section=-#

#-=Parse node properties=-#
#TEST : No node properties, 1 prop, 2 props, Mixed wih parameters
def node_properties(n, s, lnum = 0, cwd = ""):
    """
    Parses node properties

    :param n: A reference to the node (instancied object)
    :param s: Raw nodeProperties string (with no brackets)
    """

    if not s: raise ParseException(lnum, "Empty string")

    for i, e in enumerate(re.compile(r"\s*,\s*").split(s)):
        m = property_reg.match(e)
        if m is None: raise ParseException(lnum, "Parameter " + str(i) + " : Syntax error")

        #-=Let's see if we can use it=-#
        k = m.group(1) # Key
        v = m.group(2) # Optional value

        #--Existence
        if k not in nodeProperties.config: raise ParseException(lnum, "uknown node property : " + k)
        #--Retrieving config
        cfg = nodeProperties.config[k]

        #--Can be used
        if cfg.type in n.properties: raise ParseException(lnum, "Already a property with same type : " + n.properties[cfg.type][0])
        #--Allright ; let's add it to the node !
        n.properties[cfg.type] = (k, v)
        #-=End of section=-#
#-=End of section=-#

#-=Parse title=-#
#TEST : Simple title, formatted title
def node_title(n, s, lnum = 0, cwd = ""):
    """
    Parses the title of the node

    :param n: A reference to the node (instancied object)
    :param s: Raw title string
    """

    #-=Retreiving node properties=-#
    st = 0
    m = title_reg.match(s)

    if m: #Found node properties brackets []
        node_properties(n, m.group(1), lnum)
        st = m.end()
    #-=End of section=-#

    #-=Parsing title=-#
    n.title = formatted(s[st:])
    #-=End of section=-#

#-=End of section=-#

#-=Parse description=-#
#TEST : Empty desc, standard desc, raw desc
def node_desc(n, s, lnum = 0, cwd = ""):
    """
    Parses the description of the node

    :param n: A reference to the node (instancied object)
    :param s: Raw description string
    """

    if "desc" in n.properties and nodeProperties.config[n.properties["desc"][0]].raw_desc:
        if n.desc is None: n.desc = s
        else             : n.desc += "\n" + s
    else:
        if n.desc is None: n.desc = formatted(re.compile("^\s*").sub('', s))
        else                    : n.desc.append(formatted(" " + re.compile("^\s*").sub('', s)))

#-=End of section=-#

#-=Parse attachments=-#
# TEST : Exceptions, image attachment, url attachment
def node_attachment(n, s, lnum = 0, cwd = ""):
    """
    Parse a node attachment

    :param n: A reference to the node (instancied object)
    :param s: Raw attachment string
    """

    #-=Getting info=-#
    m  = attachment_reg.match(s)

    if not m: raise ParseException(lnum, "Attachment syntax error : " + repr(s))

    k  = m.group(1)
    v  = s[m.end():]
    #-=End of section=-#

    #-=Can we add it ?=-#
    if k in n.attachments: raise ParseException(lnum, "Already have an " + repr(k) + " attachment in node")
    #-=End of section=-#

    #-=Validating that shit=-#
    att = nodeAttachments.get(k)
    if att is None: raise ParseException(lnum, "Uknown attachment type : " + repr(k))
    att.input(v, cwd)
    #-=End of section=-#

    #-=Adding to node=-#
    n.attachments[k] = att
    #-=End of section=-#
#-=End of section=-#

#-=Config=-#
#TODO : DOCSTR
class LineType:
    def __init__(self):
        self.can_orphan     = False
        self.newNode        = False
        self.parse_function = None

    def chain_can_orphan(self, v):
        self.can_orphan = v
        return self

    def chain_parse_function(self, f):
        self.parse_function = f
        return self
    
    def chain_newNode(self, v):
        self.newNode = v
        return self

ltype_tab = {
    "" : LineType().chain_can_orphan(True).chain_parse_function(node_title).chain_newNode(True),
    "-": LineType().chain_can_orphan(True).chain_parse_function(node_desc).chain_newNode(True),
    "|": LineType().chain_can_orphan(False).chain_parse_function(node_desc),
    "+": LineType().chain_can_orphan(False).chain_parse_function(node_attachment)
}
#TODO : --Building ltype reg
#ltype_list = "|".join([i for i in ltype_tab.keys() if i])
#ltype_reg = re.compile("\s*(" + ltype_list + ")")
ltype_reg = re.compile("^\s*(-|\||\+)?")
#-=End of section=-#

#-=Parse global=-#
#TEST : exceptions, simple node file, complex file
def from_stream(ss):
    """
    Parses a whole tree from a stream
    :param ss: the stream to parse
    :return: the root Node() object of the parsed tree.
    """
    #TODO : Do this thing else
    cwd = os.path.dirname( os.path.realpath(ss.name) )

    #-=Alg vars=-#
    newNode                 = False # flag to know if it's a new node's context ; False 'cause root is already created
    tab_diff, tab_cur      = (0, 0)
    node_cur, node_dest, r = (None, None, None)
    #-=End of section=-#

    #-=Getting title=-#
    lnum, l    = (0, "" ) # To keep vars referenced
    for lnum, l in enumerate(ss, start = 1):
        if not is_newline(l): break;

    if not l: raise ParseException("No content...")

    #--Tablevel check
    if (tablevel(l)) > 0: raise ParseException(lnum, "Indentation error, no root node.")

    #--Creating root
    r = Node()
    node_title(r, clean_reg.sub('', l), lnum)
    node_cur = r # So that it works with the upcoming algorithm
    #-=End of section=-#

    #-=Processing loop=-#
    for lnum, l in enumerate(ss, start = lnum + 1):
        if(is_newline(l)):
            newNode = True
            continue # Skips to next line

        #-=Cleaning=-#
        l = clean_reg.sub('', l)
        #-=End of section=-#

        #-=Ltype=-#
        m     = ltype_reg.match(l)
        ltype = ltype_tab[m.group(1) if m.group(1) else ""]
        
        #--newNode
        newNode = newNode or ltype.newNode
        #-=End of section=-#

        #-=Root tab check=-#
        if newNode and tablevel(l) == 0: raise ParseException(lnum, "Cannot have two roots")
        #-=End of section=-#

        #-=Tabdiff check and find dest=-#
        ntab = {0 : (node_cur.parent(), newNode), 1: (node_cur, True)}
        tab_diff = tablevel(l) - tab_cur

        if tab_diff in ntab:
            node_dest, newNode = ntab[tab_diff]
        elif tab_diff < 0:
            newNode   = True
            node_dest = node_cur.parent().parent()
            for i in range(1, abs(tab_diff)): node_dest = node_dest.parent()
        else: #> 1
            raise ParseException(lnum, "Indent increase too wide")

        #--Remember to update tab_cur !
        tab_cur = tablevel(l)
        #-=End of section=-#

        #-=Ltype=-#
        #--orphan check
        if newNode and not ltype.can_orphan: raise ParseException(lnum, "Cannot use this line without a node context")
        #-=End of section=-#

        #-=Dest creation=-#
        if newNode:
            node_cur = node_dest.create_child()
            newNode = False
        #-=End of section=-#

        #-=Content parse=-#
        ltype.parse_function(node_cur, l[m.end():], lnum, cwd)
        #-=End of section=-#
    #-=End of section=-#

    return r
#-=End of section=-#
