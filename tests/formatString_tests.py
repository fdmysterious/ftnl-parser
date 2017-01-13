#!/usr/bin/env python

#-=Imports=-#
from formatString import FormatString
from test import *
#-=End of section=-#

#-=Chain modifiers tests=-#
test_begin("Chain modifiers")
f = FormatString()
f.chain_type("test type").chain_content("test content")

assert f.type    == "test type"
assert f.content == "test content"
###
f = FormatString().chain_type("Test Type 2").chain_content(FormatString().chain_type("test").chain_content("Hello"))

assert f.type            == "Test Type 2"
assert f.content.type    == "test"
assert f.content.content == "Hello"
test_end()
#-=End of section=-#

#-=Helpers tests=-#
test_begin("Helpers")
f = FormatString().create_plain("Test")
assert f.type    == "plain"
assert f.content == "Test"

f = FormatString().create_plain(FormatString().chain_type("test").chain_content("test"))
assert f.type            == "plain"
assert f.content.type    == "test"
assert f.content.content == "test"
###
f = FormatString().create_emph("Test")
assert f.type    == "emph"
assert f.content == "Test"

f = FormatString().create_emph(FormatString().chain_type("test").chain_content("test"))
assert f.type            == "emph"
assert f.content.type    == "test"
assert f.content.content == "test"
test_end()
#-=End of section=-#

#-=Debug print test=-#
test_begin("Debug print")
f = FormatString()
f.debug_print()
###
f = FormatString.create_plain("Hello world !")
f.debug_print()
###
f = FormatString.create_plain(FormatString.create_plain("Children content"))
f.debug_print()

f = FormatString.create_plain(FormatString.create_emph(FormatString.create_plain("Testtttt")))
f.debug_print()
###
f = FormatString.create_plain("Hello")
f.ptr_next = FormatString.create_plain(" world !")

f.debug_print()
test_end()
#-=End of section=-#

#-=Plain conversion test=-#
test_begin("Conversions")
f = FormatString()
print(f.toString())
assert f.toString() == ""

f = FormatString.create_plain("Hello world !")
print(f.toString())
assert f.toString() == "Hello world !"

f.type = "emph"
print(f.toString())
assert f.toString() == "*Hello world !*"
test_end()
#-=End of section=-#

#-=Navigation tests=-#
test_begin("Navigation")
f = FormatString()
assert f.next() == None

f = FormatString()
f.ptr_next = FormatString.create_plain("Hello")
assert f.next().content == "Hello"
########################

f = FormatString()
assert f.last() == f

f = FormatString()
f.ptr_next = FormatString.create_plain("Hello")
assert f.last() == f.next()

f = FormatString()
f.ptr_next = FormatString.create_plain("Hello world !")
f.ptr_next.ptr_next = FormatString.create_plain("This is cool")

assert f.last() == f.next().next()
test_end()
#-=End of section=-#

#-=Append test=-#
test_begin("Append")

f = FormatString()
f.append(FormatString.create_plain("Hello world"))
assert f.last().content == "Hello world"

f = FormatString.create_plain("Hello world !")
f.append(FormatString.create_emph("This is cool"))
assert f.last().content == "This is cool"

f = FormatString.create_plain(FormatString.create_plain("Hello world !"))
f.append(FormatString.create_plain("This is cool"))
assert f.last().content == "This is cool"

f = FormatString.create_plain("Hello")
f.append(FormatString.create_plain("World !"))
f.append(FormatString.create_emph("This is cool !"))
assert f.last().content == "This is cool !"
f.debug_print()

test_end()
#-=End of section=-#
