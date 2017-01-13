#!/usr/bin/env python

#-=Imports=-#
from node import Node
from formatString import FormatString
from test import *
#-=End of section=-#


#-=Navigation=-#
test_begin("Navigation")

n = Node()
assert n.parent() is None
n.ptr_parent = Node()

m = n
n.ptr_parent = m
assert n.parent() is m
###
n = Node()
assert n.children() is None

n.ptr_child = Node()
assert n.children() is n.ptr_child
###
n = Node()

assert n.next() is None
m = Node()
n.ptr_next = m
assert n.next() is m


n = Node()
m = Node()
n.ptr_child  = m
m.ptr_parent = n
assert m.first() is m
assert m.last()  is m

o = Node()
m.ptr_next = o
o.ptr_parent = n
assert o.first() is m
assert m.last()  is o

test_end()
#-=end of section=-#

#-=Child creation=-#
test_begin("Child creation")
n = Node()
m = n.create_child().chain_title(FormatString.create_plain("Test"))

assert n.children() is m

n = Node()
m = n.create_next().chain_title(FormatString.create_plain("Test2"))
assert n.last() is m
test_end()
#-=End of section=-#

#-=Debug print=-#
test_begin("Debug print")
n = Node()
n.debug_print()

n.chain_title(FormatString.create_plain("Title")).chain_desc(FormatString.create_plain("Test desc"))
n.chain_attachments({"u": "http://www.google.fr"}).chain_properties({"title": ("a", "b"), "desc": ("a", "")})
n.debug_print()

n.create_child().chain_title(FormatString.create_plain("Child")).chain_desc(FormatString.create_plain("Test desc"))
n.debug_print()

n.create_child().chain_title(FormatString.create_plain("Child2")).chain_desc(FormatString.create_plain("Test desc"))
n.debug_print()

test_end()
#-=End of section=-#
