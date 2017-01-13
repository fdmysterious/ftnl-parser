#!/usr/bin/env python

#-=Imports=-#
from formatString import FormatString
from node import Node
from output import *
from test import *

import parser
#-=End of section=-#

#-=output_formatted=-#
test_begin("Ouptut formatted")
to = TagOutput()
to.formatted_tags = {
        "plain"    : lambda s: "" + s + "",
        "emph"     : lambda s: "<e>" + s + "</e>",
        "critical" : lambda s: "<c>" + s + "</c>"}

assert to.output_formatted(FormatString.create_plain("")) == ""
assert to.output_formatted(FormatString.create_plain("Test")) == "Test"
assert to.output_formatted(FormatString.create_emph("Test")) == "<e>Test</e>"
assert to.output_formatted(FormatString.create_critical("Test")) == "<c>Test</c>"
print(str(parser.formatted("This is a *cool* test")))
print(to.output_formatted(parser.formatted("This is a *cool* test")))
assert to.output_formatted(parser.formatted("This is a *cool* test")) == "This is a <e>cool</e> test"
test_end()
#-=End of section=-#

#-=Output title=-#
test_begin("Output title")
to.title_tags = {
    "": lambda s,a,v: "<t>" + s + "</t>"
}
n = Node().chain_title("")
print(to.output_title(n))
assert to.output_title(n) == ""
n.chain_title("This is raw")
assert to.output_title(n) == "<t>This is raw</t>"
n.chain_title(parser.formatted("This is *raw*"))
print(to.output_title(n))
assert to.output_title(n) == "<t>This is <e>raw</e></t>"
test_end()
#-=End of section=-#

#-=Output description=-#
test_begin("Output desc")
to.desc_tags = {
    "" : lambda s,a,v: "<desc>" + s + "</desc>",
    "c": lambda s,a,v: "<raw>" + s + "</raw>"
}

n = Node().chain_desc("")
assert to.output_desc(n) == ""

n.chain_desc("    This is raw")
assert to.output_desc(n) == "<desc>    This is raw</desc>"

n.properties["desc"] = ("c", None)
assert to.output_desc(n) == "<raw>    This is raw</raw>"

n.properties["desc"] = ("no", None)
n.chain_desc(parser.formatted("This is *formatted*"))
assert to.output_desc(n) == "<desc>This is <e>formatted</e></desc>"
test_end()
#-=End of section=-#

#-=Output content (no child)=-#
test_begin("Output content (no child)")
to.content_tags ={
    "": lambda s,a,v: "<content>" + s + "</content>"
}

n = Node()
assert to.output_content(n) == ""

n.chain_desc(parser.formatted("This is *cool*"))
assert to.output_content(n) == "<content><desc>This is <e>cool</e></desc></content>"
test_end()
#-=End of section=-#

#-=Output node (no child)=-#
test_begin("Output node (no child)")

to.root_tags = {
    "": lambda s,a,v: "<root>" + s + "</root>"
}

to.node_tags = {
    "": lambda s,a,v: "<node>" + s + "</node>"
}

n = Node()
assert to.output_node(n) == ""

n = Node().chain_title(parser.formatted("Beautiful *test*")).chain_desc(parser.formatted("Be **cool**"))
print(repr(to.output_node(n)))
assert to.output_node(n) == "<root><t>Beautiful <e>test</e></t><content><desc>Be <c>cool</c></desc></content></root>"

n.ptr_parent = Node()
assert to.output_node(n) == "<node><t>Beautiful <e>test</e></t><content><desc>Be <c>cool</c></desc></content></node>"
test_end()
#-=End of section=-#

#-=Output children=-#
test_begin("Output children")
to.children_tags = {
    "": lambda s,a,v: "<children>" + s + "</children>"
}

n = Node()
assert to.output_children(n) == ""

n.create_child().chain_title(parser.formatted("I'm Okay"))
assert to.output_children(n) == "<children><node><t>I'm Okay</t></node></children>"
n.create_child().chain_title(parser.formatted("I'm *fine*"))
assert to.output_children(n) == "<children><node><t>I'm Okay</t></node><node><t>I'm <e>fine</e></t></node></children>"
test_end()
#-=End of section=-#

#-=Output node (children)=-#
test_begin("Output complete node")
n = Node().chain_title(parser.formatted("This is *ok*"))
n.create_child().chain_title("Hello").chain_desc(parser.formatted("Cool"))

assert to.output_node(n) == "<root><t>This is <e>ok</e></t><content><children><node><t>Hello</t><content><desc>Cool</desc></content></node></children></content></root>"
test_end()
#-=End of section=-#

