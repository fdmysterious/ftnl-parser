"""
***********************
*-=nodeProperties.py=-*
***********************

Author      : Florian Dupeyron (My?terious)
Description : Contains node properties config
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
#-=End of section=-#

#-=Class node property=-#
class NodeProperty():
    """
    Contains Definition parameters of a node property.
    """

    def __init__(self):
        #-=Attributes=-#
        """
        What does this property modify
        """
        self.type = ""

        """
        Do we need to keep the raw title (no formatting and cleaning)
        """
        self.raw_title = False

        """
        Do we need to keep the raw desc (no formatting and cleaning)
        """
        self.raw_desc = False
        #-=End of section=-#

    #-=Chain modifiers=-#
    def chain_type(self, t):
        """
        Sets the type and returns self for chaining purposes

        :param t: The new type
        :return: A self reference
        """
        self.type = t
        return self

    def chain_raw_title(self, v):
        """
        Sets the raw title and returns self for chaining purposes

        :param v: The new boolean value
        :return: A self reference
        """
        self.raw_title = v
        return self

    def chain_raw_desc(self, v):
        """
        Sets the raw desc and returns self for chaining purposes

        :param v: The new boolean value
        :return: A self reference
        """
        self.raw_desc = v
        return self
    #-=End of section=-#

#-=End of section=-#

#-=All properties definition=-#
config = {
    "l"     : NodeProperty().chain_type("children"),
    "ol"    : NodeProperty().chain_type("children"),
    "c"     : NodeProperty().chain_type("desc").chain_raw_desc(True),
    "q"     : NodeProperty().chain_type("desc"),
    "m"     : NodeProperty().chain_type("desc").chain_raw_desc(True),
    "latex" : NodeProperty().chain_type("desc").chain_raw_desc(True),
    "def"   : NodeProperty().chain_type("display"),
    "ex"    : NodeProperty().chain_type("display"),
    "info"  : NodeProperty().chain_type("display"),
    "warn"  : NodeProperty().chain_type("display"),
    "critic": NodeProperty().chain_type("display")
}
#-=End of section=-#
