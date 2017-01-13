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
import sys
import cgi # for escaping chars
from abc import ABCMeta, abstractmethod
import os

from formatString import FormatString

import latex_render
#-=End of section=-#

#-=Some config vars=-#
datadir = os.getcwd() + "/data"
#-=End of section=-#

#-=Base output class=-#
class Output(metaclass=ABCMeta):
    def __init__(self):
        pass

    #-=Functions to implement=-#
    @abstractmethod
    def output_formatted(self, s):
        """
        Outputs the formatted output.

        :param s: the formatted string to output
        :return: an outputted string
        """
        pass

    @abstractmethod
    def output_title(self, n):
        """
        Outputs the node's title

        :param n: the node to work with
        :return: an outputted string
        """
        pass

    @abstractmethod
    def output_desc(self, n):
        """
        Outputs the node's description

        :param n: the node to work with
        :return: an outputted string
        """
        pass

    @abstractmethod
    def output_node(self, n):
        """
        Outputs a node

        :param n: the node to work with
        :return: an outputted string
        """
        pass
    #-=End of section=-#
#-=End of section=-#

#-=DefaultOutput=-#
#--Exceptions
class NotSupportedException(Exception):
    def __init__(self, what):
        self.what = what

class TagOutput(Output):
    def __init__(self):
        #-=Tags tab=-#
        self.formatted_tags = {}
        self.title_tags     = {}
        self.desc_tags      = {}
        self.content_tags   = {}
        self.children_tags  = {}
        self.node_tags      = {}
        self.root_tags      = {}
        #-=End of section=-#

    def _ocfg(self, s, n, cfg, p, default = ""):
        """
        Generic function to outputs content from config and node properties

        :param s:       the string to output
        :param n:       the current node
        :param cfg:     tag config to use
        :param p:       property type that affects current content
        :param default: default type if not supported
        """
        if not s: return ""
        k, v = n.properties[p] if p in n.properties else (default, "") # k is node property key, v optional value
        o = cfg[default] if not k in cfg else cfg[k]
        if not k in cfg: print("-> Unsupported node property " + repr(k) + ", using default", file=sys.stderr)
        return o(s, n.attachments, v)
    
    #-=Output functions=-#
    #TEST : Empty string, Formatted string with some tags
    def output_formatted(self, s):
        e = s
        r = ""
        
        if(type(s) == type("")): return s
        else:
            while e is not None:
                #-=Getting config=-#
                o = self.formatted_tags[e.type if e.type in self.formatted_tags else "plain"]
                if not e.type in self.formatted_tags: print("-> Unspecified formatted element " + repr(e.type) + ", using default", file=sys.stderr)
                #-=End of section=-#

                #-=Append content=-#
                r += o(self.output_formatted(e.content))
                #-=End of section=-#

                e = e.next()
        return r
    
    #TEST : Empty title, Simple title, Formatted title
    def output_title(self, n): return self._ocfg(self.output_formatted(n.title), n, self.title_tags, "display")
    #TEST : Empty desc, Raw desc, Formatted desc
    def output_desc (self, n): return self._ocfg(self.output_formatted(n.desc) , n, self.desc_tags , "desc")
    #TEST : No Children, children ; NOTE : Test with children after output_node with no children
    def output_children(self, n):
        r = ""
        e = n.children()
        while e is not None:
            r += self.output_node(e)
            e = e.next()
        return self._ocfg(r, n, self.children_tags, "children")
    def output_content(self, n):
        r = self.output_desc(n) + self.output_children(n)
        return self._ocfg(r, n, self.content_tags, "display")

    #TEST : Simple node (with no content), node with children ; NOTE : Test with children after output_children with children
    def output_node(self, n):
        r = self.output_title(n) + self.output_content(n)
        return self._ocfg(r, n, self.node_tags if n.parent() else self.root_tags, "display")
    #-=End of section=-#
#-=End of section=-#

#TODO : Special folder for custom output modules
#-=HTML Output module=-#
class HTMLOutput(TagOutput):
    def __init__(self):
        super(TagOutput).__init__()
        
        #-=Tags tab=-#
        self.formatted_tags = {
            "plain"   : lambda s: s,
            "emph"    : lambda s: "<em>" + s + "</em>",
            "critical": lambda s: "<strong>" + s + "</strong>",
            "math"    : lambda s: "<img alt='" + s + "' src='" + "data" + latex_render.png.render("$" + s + "$", datadir) + "'/>"
        }

        self.title_tags = {
            "": lambda s,a,v: "<div class='title'>" + s + "</div>"
        }

        self.desc_tags  = {
            "" : lambda s,a,v: s,
            "c": lambda s,a,v: "<pre>" + s + "</pre>",
            "q": lambda s,a,v: "<blockquote>" + s + "</blockquote>",
            "m": lambda s,a,v: "<img alt='" + s + "' src='" + "data" + latex_render.png.render("\\[" + s + "\\]", datadir) + "'/>"
        }

        self.children_tags = {
            ""  : lambda s,a,v: "<ul class='no-bullets'>" + s + "</ul>",
            "l" : lambda s,a,v: "<ul>" + s + "</ul>",
            "ol": lambda s,a,v: "<ol>" + s + "</ol>"
        }

        self.content_tags = {
            "": lambda s,a,v: "<div class='content'>" + s + "</div>"
        }

        self.node_tags = {
            "": lambda s,a,v: "<li>" + s + "</li>"
        }

        self.root_tags = {
            "": lambda s,a,v: "<!DOCTYPE html><html><head><meta charset='utf-8'/><link rel='stylesheet' href='style.css'/><title>FTNL Map</title></head><body>" + s + "</body></html>"
        }
        #-=End of section=-#
#-=End of section=-#

#-=MMap Output module=-#
class MMapOutput(TagOutput):
    def __init__(self):
        super(TagOutput).__init__()

        #-=Tags tabs=-#
        self.formatted_tags = {
            "plain"   : lambda s: s,
            "emph"    : lambda s: "<b>{0}</b>".format(s),
            "critical": lambda s: "<b>{0}</b>".format(s),
            "math"    : lambda s: "<img alt='" + s + "' src='" + "data" + latex_render.png.render("$" + s + "$", datadir) + "'/>"
        }

        self.title_tags     = {
                "": lambda s,a,v: "<h3>{0}</h3>{1}".format(s, '<img src="{0}"/>'.format(a["i"].path) if "i" in a else "")
        }

        self.desc_tags = {
            "" : lambda s,a,v: '<div class="desc">{0}</div>'.format(s),
            "c": lambda s,a,v: self.desc_tags[""]("<pre>{0}</pre>".format(s), a, v),
            "q": lambda s,a,v: self.desc_tags[""]("<blockquote>{0}</blockquote>".format(s), a, v),
            "m": lambda s,a,v: "<img alt='" + s + "' src='" + "data" + latex_render.png.render("\\[" + s + "\\]", datadir) + "'/>", #TODO : more elegant way to redirect to data folder
            "latex": lambda s,a,v: "<img alt='tabular' src='" + "data" + latex_render.png.render(s, datadir) + "'/>"
        }

        self.content_tags = {
            "": lambda s,a,v: '<richcontent TYPE="NODE"><html><head></head><body>{0}</body></html></richcontent>'.format(s)
        }

        self.children_tags = {
            "": lambda s,a,v: s
        }

        self.node_tags = {
            "": lambda s,a,v: '<node {1}FOLDED="true">{0}</node>'.format(s, 'LINK="{0}" '.format(str(a["u"])) if "u" in a else "")
        }

        self.root_tags = {
            "": lambda s,a,v: '<map version="1.0.1">{0}</map>'.format(self.node_tags[""](s,a,v))
        }
        #-=End of section=-#

    def output_node(self, n):
        r = ""
        r += self._ocfg(self.output_title(n) + self.output_desc(n), n, self.content_tags, "display", "")
        r += self.output_children(n)

        return self._ocfg(r, n, self.node_tags if n.ptr_parent else self.root_tags, "display")
#-=End of section=-#

#-=Special Freeplane output module=-#
class FreeplaneOutput( TagOutput ):
    def __init__(self):
        super( TagOutput ).__init__()

        #-=Tags tabs=-#
        self.formatted_tags = {
            "plain"    : lambda s: s,
            "emph"     : lambda s: "\\textbf{{ {0} }}".format(s),
            "critical" : lambda s: "\\large{{ \\textbf{{ {0} }} }}".format(s),
            "math"     : lambda s: "${0}$".format(s)
        }

        self.title_tags     = {
            "" : lambda s,a,v : "\\Large{{ {0} }}\\\\{1}".format( s, "\\includegraphics[width=10cm]{{{0}}}\\\\".format(a["i"].path) if "i" in a else "")
        }

        self.desc_tags      = {
            "" : lambda s,a,v: s,
            "c": lambda s,a,v: s,
            "q": lambda s,a,v: "``\\textit{{ {0} }}''".format(s),
            "m": lambda s,a,v: "\\[{0}\\]".format(s),
            "latex": lambda s,a,v:s
        }

        self.content_tags   = {
            "": lambda s,a,v: s
        }

        self.children_tags = {
            "": lambda s,a,v: s
        }

        #self.node_tags = {
        #    "": lambda s,a,v: '<node {1}FOLDED="true" TEXT="" FORMAT="latexPatternFormat">{0}</node>'.format( replace('"', '\\"'), 'LINK="{0}" '.format( str(a["u"]) ) if "u" in a else "" )
        #}
        self.node_tags = {
            "": lambda s,a,v,t: '<node {1}FOLDED="true" TEXT="{1}" FORMAT="latexPatternFormat">{0}</node>'.format( cgi.escape(s), 'LINK="{0}"'.format( str(a["u"]) ) if "u" in a else "", t )
        }

        #self.root_tags = {
        #    "": lambda s,a,v: '<map version="freeplane 1.3.0">{0}</map>'.format(self.node_tags[""](s,a,v))
        #}

        self.root_tags = {
            "": lambda s,a,v,t: '<map version="freeplane 1.3.0">{0}</map>'.format(self.node_tags[""](s,a,v,t))
        }
        ##-=End of section=-#

    def output_node( self, n ):
        #TODO : More modular architecture
        t = self._ocfg( self.output_title(n) + self.output_desc(n), n, self.content_tags, "display", "" )
        c = self.output_children(n)

        #return self._ocfg(r, n, self.node_tags if n.ptr_parent else self.root_tags, "display")
        return self.node_tags[""]( c, n.attachments, None, t )

#-=End of section=-#:
