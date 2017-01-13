#!/usr/bin/env python

#-=Imports=-#
import parser
from formatString import FormatString
import nodeProperties
import nodeAttachments
from node import Node
from test import *
#-=EOS=-#

#-=Utilty functions=-#
test_begin("Utilty functions")
assert parser.tablevel("")                             == 0
assert parser.tablevel("	")                     == 1
assert parser.tablevel("		")             == 2
assert parser.tablevel("		Test content") == 2

assert parser.is_newline("")             == True
assert parser.is_newline("   ")          == True
assert parser.is_newline("	")       == True
assert parser.is_newline("   Test loul") == False
test_end()
#-=End of section=-#

#-=parse_formatted=-#
test_begin("Parse formatted")
assert parser.formatted("").content == ""
parser.formatted("Hello World !").debug_print()
parser.formatted("Hello world with some *important* and **critical** content").debug_print()
test_end()
#-=EOS=-#

#-=parse node properties=-#
test_begin("Parse node properties")
n = Node()
try : parser.node_properties(n, "")
except parser.ParseException as e : print(str(e))

parser.node_properties(n, "c")
assert n.properties == {"desc": ("c", None)}
print(repr(n.properties))

n = Node()
parser.node_properties(n, "c,l")
assert n.properties == {"desc": ("c", None), "children": ("l", None)}
print(repr(n.properties))

n = Node()
parser.node_properties(n, "c=t,l")
assert n.properties == {"desc": ("c", "t"), "children": ("l", None)}
print(repr(n.properties))

n = Node()
try : parser.node_properties(n, "l = t, ol")
except parser.ParseException as e : print(str(e))

n = Node()
try : parser.node_properties(n, "l, i = u")
except parser.ParseException as e: print(str(e))

try : parser.node_properties(n, "l = i = u; kghqsosz")
except parser.ParseException as e: print(str(e))
test_end()
#-=End of section=-#

#-=parse title=-#
test_begin("Parse title")
n = Node()
parser.node_title(n, "This is cool")
n.title.debug_print()

n = Node()
parser.node_title(n, "This is *very* cool")
n.title.debug_print()

n = Node()
parser.node_title(n, "[l, c=t] This is **very very** cool !")
n.title.debug_print()
print(repr(n.properties))
test_end()
#-=End of section=-#

#-=Parse description=-#
#Standard (no property)
n = Node()
parser.node_desc(n, "    Testifying things")
n.desc.debug_print()

n = Node()
parser.node_desc(n, "   Testifying *a lot of* things")
n.desc.debug_print()

parser.node_desc(n, "lol")
n.desc.debug_print()

#Standard (with property)
n = Node().chain_properties({"desc": ("q", None)})
parser.node_desc(n, "    Testifying things")
n.desc.debug_print()

n = Node().chain_properties({"desc": ("q", None)})
parser.node_desc(n, "    Testyfying with *things*")
n.desc.debug_print()

parser.node_desc(n, "adding *thingssssss* lel")
n.desc.debug_print()

#Raw
n = Node().chain_properties({"desc": ("c", None)})
parser.node_desc(n, "    Testifying things")
assert n.desc    == "    Testifying things"

n = Node().chain_properties({"desc": ("c", None)})
parser.node_desc(n, "    Some *useless* code")
assert n.desc    == "    Some *useless* code"
parser.node_desc(n, "  Adding things lel")
print(repr(n.desc))
assert n.desc    == "    Some *useless* code\n  Adding things lel"
#-=End of section=-#

#-=Parse Attachments=-#
test_begin("Parse attachments")

#Exception test : bad syntax
n = Node()
try:   parser.node_attachment(n, "sf = lol")
except parser.ParseException as e: print(str(e))

#Exception test : Already have an attachment
n = Node().chain_attachments({"a": ""})
try: parser.node_attachment(n, "a b")
except parser.ParseException as e: print(str(e))

#Exception test : uknown attachment type
n = Node()
try: parser.node_attachment(n, "a b")
except parser.ParseException as e: print(str(e))

#Image attachment
n = Node()
parser.node_attachment(n, "i test.jpg")
print(repr(n.attachments))
assert n.attachments["i"].path == "test.jpg"

#Not valid image attachment
n = Node()
try: parser.node_attachment(n, "i notfound.jpg")
except nodeAttachments.ValidateException as e: print(str(e))

#Not valid path image attachment
n = Node()
try: parser.node_attachment(n, "i ht://gùsjueg/oh()ndfg LEL")
except nodeAttachments.ValidateException as e: print(str(e))

#Url attachment
n = Node()
parser.node_attachment(n, "u http://mugcat.fr")

#Not valid URL Attachment
#TODO

test_end()
#-=End of section=-#

#-=Parse stream tests=-#
n = Node()

#--Exceptions
with open("nf/empty", "r") as f:
    try: n = parser.from_stream(f)
    except parser.ParseException as e: print(str(e))

with open("nf/noroot", "r") as f:
    try: n = parser.from_stream(f)
    except parser.ParseException as e: print(str(e))

with open("nf/tworoots", "r") as f:
    try: n = parser.from_stream(f)
    except parser.ParseException as e: print(str(e))

with open("nf/indenterr", "r") as f:
    try: n = parser.from_stream(f)
    except parser.ParseException as e: print(str(e))

with open("nf/orphanerr", "r") as f:
    try: n = parser.from_stream(f)
    except parser.ParseException as e: print(str(e))

#--Simple file
with open("nf/simple", "r") as f:
    n = parser.from_stream(f)
    n.debug_print()

#--Complex file
with open("nf/complex", "r") as f:
    n = parser.from_stream(f)
    n.debug_print()
#-=End of section=-#

#-=Buggy file=-#
with open("nf/releve_intro.nf", "r") as f:
    n = parser.from_stream(f)
    n.debug_print()
#-=End of section=-#
