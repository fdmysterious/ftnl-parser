"""
************************
*-=nodeAttachments.py=-*
************************

Author      : Florian Dupeyron (My?terious)
Description : Configuration of node Attachments
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
import os
import copy
import re
#-=End of section=-#

class ValidateException(Exception):
    def __init__(self, att, v):
        self.att  = att
        self.v    = v

    def __str__(self):
        return "Cannot validate attachment : " + self.v

class Attachment:
    def __init__(self):
        pass

    def input(self, v, cwd):
        """
        Functions that validates and store the value passed to the attachment

        :param v: The raw value string
        :param cwd: current working directory
        """
        pass
    
    def __str__(self):
        return "attachement"

#-=Url validatation regex=-#
url_validate_regex = re.compile("^https?://(\w+\.)+(\w+)$")
#-=End of section=-#
class UrlAttachment(Attachment):
    def __init__(self):
        self.url = ""

    def input(self, v, cwd):
        #TODO : url validation
        if not url_validate_regex.match(v): raise ValidateException(self, "Invalid url : " + repr(v))
        self.url = v

    def __str__(self):
        return self.url

class FileAttachment(Attachment):
    def __init__(self):
        self.path = ""

    def input(self, v, cwd):
        #-=Determining real path=-#
        p = os.path.join(cwd if not os.path.isabs(v) else "", v)
        #-=End of section=-#

        if not os.path.isfile(p): raise ValidateException(self, "File " + repr(p) + "doesn't exist")
        self.path = p

class ImageAttachment(FileAttachment):
    def __init__(self):
        super(FileAttachment, self).__init__()

    def __str__(self):
        return "+ i " + self.path

#-=Config tab=-#
#TODO Add :
# v : video
# s : sound

config = {
    "i": ImageAttachment(),
    "f": FileAttachment(),
    "u": UrlAttachment()
}
#-=End of section=-#

#-=Get func=-#
def get(k):
    """
    Returns a copy of an attachment given its key
    :param k: the key of the attachment
    :return: A copy of the attachment class or None if not found
    """

    if k in config: return copy.copy(config[k])
    else: return None
#-=End of section=-#
