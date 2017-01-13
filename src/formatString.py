"""
*********************
*-=formatString.py=-*
*********************

Author      : Florian Dupeyron (My?terious)
Description : Class to store a formatted string
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
import weakref
#-=End of section=-#

class FormatString:
    #-=Constructor=-#
    def __init__(self):
        #-=Attributes=-#
        """
        A string used to identify the token type
        """
        self.type = ""

        """
        The content of the string. Can be a standard string
        or an other FormatString so that we can combine formats
        """
        self.content = ""

        self.ptr_next = None
        #-=End of section=-#
    #-=End of section=-#

    #-=Bool=-#
    def __bool__(self):
        return self.content != "" 
    #-=End of section=-#

    #-=Chain modifiers=-#
    def chain_type(self, t):
        """
        Sets the type and return self for chaining purposes.

        :param t: The new token type to assign.
        :return: A self reference
        """
        self.type = t
        return self

    def chain_content(self, c):
        """
        Sets the content and return self for chaining purposes.

        :param c: The new token's content
        :return: A self reference
        """
        self.content = c
        return self
    #-=End of section=-#

    #-=Normal modifiers=-#
    #TEST : Add with no content, with string content and with FormatString content
    def append(self, c):
        """
        Appends new content at the end of this string
        :param c: The content to add
        :return: A reference to the last added element
        """

        #-=Creating FormatString if necessary=-#
        if not self.content:
            #TODO : Optimize
            self.content = c.content
            self.type    = c.type
            self.ptr_next = None

            return self
        #-=End of section=-#

        #-=Adding new content=-#
        l = self.last()
        l.ptr_next = c # Using ptr_next to keep a valid ref
        #-=End of section=-#

        return l.next()

    #-=End of section=-#

    #-=Navigation=-#
    #TEST : 1 next, 0 next
    def next(self):
        """
        Returns a reference to next string token. Here for writing
        consistency. Avoid using ptr_next directly.
        :return: A reference to the next string token or None if end of string.
        """
        return self.ptr_next

    #TEST : 0 next, 1 net, 2 next
    def last(self):
        """
        Returns a reference to the last string token.
        :return: A reference to the last string token
        """
        s = self
        while s.next() is not None: s = s.next()

        return s
    #-=End of section=-#

    #-=Helpers=-#
    #TODO : Better managment of these functions
    @staticmethod
    def create_plain(content):
        """
        Creates a plain format string and returns it

        :param content: The content of the new string
        :return: A plain FormatString
        """
        return FormatString().chain_type("plain").chain_content(content)

    @staticmethod
    def create_emph(content):
        """
        Creates a bold format string and returns it

        :param content: The content of the new string
        :return: A bold FormatString
        """
        return FormatString().chain_type("emph").chain_content(content)

    @staticmethod
    def create_critical(content):
        """
        Creates a critical format string and returns it

        :param content: New string's content
        :return: FormatString
        """
        return FormatString().chain_type("critical").chain_content(content)

    @staticmethod
    def create_math(content):
        """
        Creates a math format string and returns it

        :param content: New string's content
        :return: FormatString
        """
        return FormatString().chain_type("math").chain_content(content)
    #-=End of section=-#

    #-=Conversion=-#
    #TEST : Empty, string with 1 plain, string with 1 bold, string with both,
    #string with imbriqued content
    def toString(self):
        """
        Converts a FormatString to a standard string using FTNL code
        :return: a standard string
        """
        t  = {"plain": "", "emph": "*", "": "", "critical": "**", "math": "$"} #TODO : move that elsewhere.
        r = ""
        n = self

        while n is not None:
            r += " " if len(r) else ""
            c = n.content.toString() if type(n.content) == type(FormatString()) else n.content
            r += t[n.type] + c + t[n.type]
            n = n.next()

        return r

    def __str__(self):
        return self.toString()
    #-=End of section=-#

    #-=Debug functions=-#
    #TEST : Empty string, string with 1 plain element, string with two elements,
    # string with imbriqued elements
    #def debug_print(self, newline = True):
    #    n = self
    #    while n is not None:
    #        if type(n.content) == type(FormatString()): n.content.debug_print(False)
    #        else: print(n.content, end="")
    #        n = n.next()
    #    if(newline): print()

    def debug_print(self, newline = True):
        print(self.toString())
        print()
    #-=End of section=-#
