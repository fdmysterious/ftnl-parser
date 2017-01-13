"""
*************
*-=node.py=-*
*************

Author      : Florian Dupeyron (My?terious)
Description : Class to store info about a node.
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
from formatString import FormatString
#-=End of section=-#

class Node:
    #-=Constructor=-#
    def __init__(self):
        #-=Attributes=-#
        self.title          = None 
        self.desc           = None
        self.attachments    = {}
        self.properties     = {}
        
        self.ptr_next       = None
        self.ptr_parent     = None
        self.ptr_child      = None
        #-=End of section=-#

    #-=End of section=-#

    #-=Chain modifiers=-#
    def chain_title(self, title):
        """
        Sets the title and returns self for chaining purposes.

        :param title: the new title for the node
        :return: a self reference
        """

        self.title = title
        return self

    def chain_desc(self, desc):
        """
        Sets the desccription and returns self for chaining purposes.

        :param desc: the new description for the node
        :return: a self reference
        """
        self.desc = desc
        return self

    def chain_attachments(self, attachments):
        """
        Sets the attachments and returns self for chaining purposes.

        :param attachments: the new attachments for the node
        :return: a self reference
        """
        self.attachments = attachments
        return self

    def chain_properties(self, properties):
        """
        Sets the node properties and returns self for chaining purposes.

        :param nodeProperties: the new properties for the node
        :return: a self reference
        """
        self.properties = properties
        return self
    #-=End of section=-#

    #-=Navigation=-#
    #TEST : Parent and no parent
    def parent(self):
        """
        Returns a ref to the parent node.
        This function is more here for writing consistency. Avoid using
        ptr_parent directly.

        :return: A reference to the parent node or None if root node 
        """
        return self.ptr_parent

    #TEST : 1 child, 2 child, and no child
    def children(self):
        """
        Returns a ref to the first child
        This function is more here for writing consistency. Avoid using
        ptr_child directly.

        :return: A reference to the first child or None if no children
        """
        return self.ptr_child

    #TEST : 1 next, 2 next and no next
    def next(self):
        """
        Returns a ref to the next element of the chained list
        This function is more here for writing consistency. Avoid using
        ptr_next directly.

        :return: A reference to the next node or None if last node.
        """
        return self.ptr_next

    #TEST : 1 node, 2 nodes, 3 nodes
    def first(self):
        """
        Returns the first node of the chained list
        """
        n = self
        p = self.parent()
        if p is not None: n = p.children()
        return n

    #TEST : 1 node, 2 nodes, 3 nodes
    def last(self):
        """
        Returns the last node of the chained list

        :return: A reference to the last node of the chained list
        """
        n = self
        while n.next() is not None: n = n.next()
        return n
    #-=End of section=-#

    #-=Children création=-#
    #TEST : child creation
    def create_child(self):
        """
        Creates a child and append it to the chained list
        :return: a reference to the new child
        """

        #-=Creating node=-#
        m = Node()
        m.ptr_parent = self 
        #-=End of section=-#

        #-=Adding to tree=-#
        if self.children() is None: self.ptr_child = m
        else: self.children().last().ptr_next      = m
        #-=End of section=-#

        return m

    def create_next(self):
        """
        Creates a node at the end of the chained list
        :return: a ref to the new node
        """

        #-=Creating node=-#
        m = Node()
        m.ptr_parent = self.ptr_parent
        #-=End of section=-#

        #-=Append to tree=-#
        self.last().ptr_next = m
        #-=End of section=-#

        return m
    #-=End of section=-#

    #-=Debug print=-#
    #TEST : Empty node, Full content, Empty with child, full with child
    def debug_print(self, lvl = 0):
        #-=Print level=-#
        tab = ""
        for i in range(0, lvl): tab += "    "
        #-=End of section=-#
        
        #-=Print content=-#
        if(self.title): print(tab + repr(str(self.title)))
        for k,v in self.attachments.items(): print(tab + "+" + k + " : " + str(v))
        for k,(v, w) in self.properties.items():   print(tab + "[" + v + "=" + (w if w else "None") + "] : " + k)
        if(self.desc): print(tab + "| " + repr(str(self.desc)))
        #-=End of section=-#

        #-=Print children=-#
        if(self.children() is not None): self.children().debug_print(lvl + 1)
        #-=End of section=-#

        #-=Print next=-#
        if(self.next() is not None): self.next().debug_print(lvl)
        #-=End of section=-#
    #-=End of section=-#
